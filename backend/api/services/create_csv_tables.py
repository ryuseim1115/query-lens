import duckdb


def create_csv_tables(csv_info):
    con = duckdb.connect()
    for csv_file in csv_info.csv_files:
        table_name = csv_file.removesuffix(".csv")
        con.sql(
            f"CREATE TABLE '{table_name}' AS SELECT * FROM '{csv_info.CSV_FILES_DIR}/{csv_file}'"
        )
        con.table(table_name).show()
    con.sql("show tables").show()
