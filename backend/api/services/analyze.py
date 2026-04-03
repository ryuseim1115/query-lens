import sqlglot
from sqlglot import exp


def analyze(query):

    parsed = sqlglot.parse_one(query)
    tables = []
    for table in parsed.find_all(exp.Table):
        tables.append(table.sql())

    print(query)
    print(set(tables))
    return set(tables)
