import sqlglot
from sqlglot import exp


def extract_tables_with_alias(query: str) -> list[tuple[str | None, str | None]]:
    query = query.strip()
    if query.startswith("(") and query.endswith(")"):
        query = query[1:-1].strip()
    try:
        expression = sqlglot.parse_one(query)
    except Exception:
        return []

    tables = []
    from_expr = expression.args.get("from_")
    if from_expr:
        table_name_alias = _get_table_info(from_expr.this)
        if any(table_name_alias):
            tables.append(table_name_alias)

    for join in expression.args.get("joins") or []:
        table_name_alias = _get_table_info(join.this)
        if any(table_name_alias):
            tables.append(table_name_alias)

    return tables


def _get_table_info(node) -> tuple[str | None, str | None]:
    """(table_name, alias) を返す。"""
    if isinstance(node, exp.Table):
        return node.name or None, node.alias or None
    if isinstance(node, exp.Subquery):
        return None, node.alias or None
    return None, None
