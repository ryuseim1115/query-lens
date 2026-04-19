import sqlglot
from sqlglot import parse_one, errors


class QueryValidator:
    def __init__(self, database_type: str, query: str):
        self.database_type = database_type
        self.query = query

    def validate(self) -> sqlglot.Expression:
        try:
            expression = parse_one(self.query, read=self.database_type)
        except errors.ParseError as e:
            raise ValueError(f"SQL構文が正しくありません: {str(e)}")

        if expression.key != "select":
            raise ValueError("SELECT文以外の実行は許可されていません。")

        return expression
