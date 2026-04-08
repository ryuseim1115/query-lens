import sqlglot
from sqlglot import exp


def analyze(query):
    parsed = sqlglot.parse_one(query)
    tables = [table.name for table in parsed.find_all(exp.Table)]

    for join in parsed.find_all(exp.Join):
        target_table = join.find(exp.Table)

        target_name = (
            target_table.sql()
            if target_table
            else (join.this.sql() if join.this else "Subquery/Other")
        )
        tables.append(target_name)
        join_type = join.args.get("kind") or "INNER"
        on_condition = join.find(exp.Condition)
        on_sql = on_condition.sql() if on_condition else "No Condition"

    return tables
