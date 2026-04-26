"""実テーブル同士の JOIN について、行対応つきプレビューデータを組み立てる。"""

from __future__ import annotations

import sqlglot
from sqlglot import exp

from api.db.connection import get_connection
from api.schemas.run_query import JoinInfo, JoinLinkRow, JoinPreview

_PREVIEW_LIMIT = 40


def _row_get(row: dict, col: str) -> object:
    if col in row:
        return row[col]
    cl = col.lower()
    for k, v in row.items():
        if str(k).lower() == cl:
            return v
    return None


def _has_columns(sample_row: dict, keys: list[str]) -> bool:
    lower_keys = {str(k).lower() for k in sample_row}
    return all(k.lower() in lower_keys for k in keys)


def _extract_equality_column_pairs(on_sql: str, left_alias: str, right_alias: str) -> list[tuple[str, str]]:
    if not on_sql or not on_sql.strip():
        return []
    la = left_alias.lower()
    ra = right_alias.lower()
    tree = sqlglot.parse_one(on_sql)
    out: list[tuple[str, str]] = []
    for eq in tree.find_all(exp.EQ):
        if not isinstance(eq.left, exp.Column) or not isinstance(eq.right, exp.Column):
            continue
        lt = (eq.left.table or "").strip('"').lower()
        rt = (eq.right.table or "").strip('"').lower()
        if lt == la and rt == ra:
            out.append((eq.left.name.strip('"'), eq.right.name.strip('"')))
        elif lt == ra and rt == la:
            out.append((eq.right.name.strip('"'), eq.left.name.strip('"')))
    return out


def _fetch_table_rows(table: str | None, subquery_sql: str | None) -> list[dict]:
    if subquery_sql:
        q = f'SELECT * FROM ({subquery_sql}) t LIMIT {_PREVIEW_LIMIT}'
    elif table is not None:
        escaped = table.replace('"', '""')
        q = f'SELECT * FROM "{escaped}" LIMIT {_PREVIEW_LIMIT}'
    else:
        return []
    rel = get_connection().sql(q)
    return [dict(zip(rel.columns, row)) for row in rel.fetchall()]


def _compute_links(
    left_rows: list[dict],
    right_rows: list[dict],
    left_keys: list[str],
    right_keys: list[str],
) -> list[JoinLinkRow]:
    return [
        JoinLinkRow(
            left_row=i,
            right_rows=[
                j for j, rr in enumerate(right_rows)
                if all(_row_get(lr, lk) == _row_get(rr, rk) for lk, rk in zip(left_keys, right_keys))
            ],
        )
        for i, lr in enumerate(left_rows)
    ]


class JoinPreviewBuilder:
    def __init__(self, subqueries: list) -> None:
        self.subqueries = subqueries

    def execute(self) -> list:
        for subquery in self.subqueries:
            subquery.join_previews = [self._build_one(j) for j in subquery.joins]
        return self.subqueries

    @staticmethod
    def _build_one(join: JoinInfo) -> JoinPreview | None:
        if not join.on:
            return None
        if not join.left_table and not join.left_subquery:
            return None
        if not join.right_table and not join.right_subquery:
            return None

        pairs = _extract_equality_column_pairs(join.on, join.left_alias, join.right_alias)
        if not pairs:
            return None

        left_keys = [p[0] for p in pairs]
        right_keys = [p[1] for p in pairs]

        try:
            left_rows = _fetch_table_rows(join.left_table, join.left_subquery)
            right_rows = _fetch_table_rows(join.right_table, join.right_subquery)
        except Exception:
            return None

        if not left_rows or not right_rows:
            return None
        if not _has_columns(left_rows[0], left_keys) or not _has_columns(right_rows[0], right_keys):
            return None

        left_columns = list(left_rows[0].keys())
        right_columns = list(right_rows[0].keys())
        links = _compute_links(left_rows, right_rows, left_keys, right_keys)

        return JoinPreview(
            left_title=join.left_table or join.left_alias,
            right_title=join.right_table or join.right_alias,
            left_columns=left_columns,
            right_columns=right_columns,
            left_join_columns=left_keys,
            right_join_columns=right_keys,
            left_rows=left_rows,
            right_rows=right_rows,
            links=links,
        )
