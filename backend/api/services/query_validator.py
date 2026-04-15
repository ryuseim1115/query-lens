from sqlglot import parse_one, errors


class QueryValidator:
    def __init__(self, database_type, query):
        self.database_type = database_type
        self.query = query
        self.is_valid = True
        self.error_msg = ""
        self.expression = None
        self.is_valid_syntax()
        self.is_select_query()

    def is_valid_syntax(self):
        try:
            self.expression = parse_one(self.query, read=self.database_type)
        except errors.ParseError as e:
            self.is_valid = False
            self.error_msg = f"SQL構文が正しくありません: {str(e)}"

    def is_select_query(self):
        if self.expression and self.expression.key != "select":
            self.is_valid = False
            self.error_msg = "SELECT文以外の実行は許可されていません。"
