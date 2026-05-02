from api.db.connection import get_connection


def create_csv_tables(csv_files_dir: str, csv_files: list[str]):
    connection = get_connection()
    for csv_file in csv_files:
        table_name = csv_file.removesuffix(".csv")
        connection.sql(
            f"CREATE OR REPLACE TABLE \"{table_name}\" AS SELECT * FROM '{csv_files_dir}/{csv_file}'"
        )
