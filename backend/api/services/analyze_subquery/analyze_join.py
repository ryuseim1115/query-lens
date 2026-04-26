from dataclasses import dataclass
import sqlglot
from sqlglot import exp

from api.schemas.run_query import JoinInfo


@dataclass
class TableInfo:
    alias: str | None
    table_name: str | None
    subquery: str | None


def extract_from_info(query: str) -> tuple[str | None, str | None, str | None]:
    """FROMの (alias, physical_table, subquery_sql) を返す。"""
    query = query.strip()
    if query.startswith("(") and query.endswith(")"):
        query = query[1:-1].strip()
    try:
        expression = sqlglot.parse_one(query)
    except Exception:
        return None, None, None
    from_expr = expression.args.get("from_")
    if not from_expr:
        return None, None, None
    info = _get_table_info(from_expr.this)
    return info.alias, info.table_name, info.subquery


def extract_joins(query: str) -> list[JoinInfo]:
    query = query.strip()
    if query.startswith("(") and query.endswith(")"):
        query = query[1:-1].strip()
    try:
        expression = sqlglot.parse_one(query)
    except Exception:
        return []

    from_expr = expression.args.get("from_")
    if not from_expr:
        return []

    joins = []
    left_rel = _get_table_info(from_expr.this)

    for join in expression.args.get("joins") or []:
        right_rel = _get_table_info(join.this)
        if left_rel.alias and right_rel.alias:
            on_expr = join.args.get("on")
            joins.append(
                JoinInfo(
                    left_alias=left_rel.alias,
                    right_alias=right_rel.alias,
                    join_type=_join_type(join),
                    on=on_expr.sql() if on_expr else None,
                    left_table=left_rel.table_name,
                    right_table=right_rel.table_name,
                    left_subquery=left_rel.subquery,
                    right_subquery=right_rel.subquery,
                )
            )
        left_rel = right_rel

    return joins


def _get_table_info(node) -> TableInfo:
    if isinstance(node, exp.Table):
        return TableInfo(alias=node.alias or node.name, table_name=node.name, subquery=None)
    if isinstance(node, exp.Subquery):
        return TableInfo(alias=node.alias or "(subquery)", table_name=None, subquery=node.this.sql())
    return TableInfo(alias=None, table_name=None, subquery=None)


def _join_type(join: exp.Join) -> str:
    side = join.args.get("side") or ""
    kind = join.args.get("kind") or ""
    if side:
        return str(side)
    if kind and str(kind).upper() not in ("JOIN", "INNER", ""):
        return str(kind).upper()
    return "INNER"
