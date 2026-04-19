import duckdb

_con = duckdb.connect()


def get_connection() -> duckdb.DuckDBPyConnection:
    return _con
