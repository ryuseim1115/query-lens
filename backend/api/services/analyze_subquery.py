import sqlglot


class AnalyzeSubquery:
    def __init__(self, query):
        self.query = query
        self.tokens = sqlglot.tokens.Tokenizer().tokenize(self.query)
        self.subquery_ranges = self.find_subquery_ranges()
        self.subquery_texts = self.get_subquery_texts()
        self.subquery_depths = self.get_subquery_depths()

    def find_subquery_ranges(self) -> list[tuple[int, int]]:
        if not self.tokens:
            return []
        ranges = []
        stack = []  # (の開始位置を保持する（サブクエリでなければ False）
        T = sqlglot.tokens.TokenType
        for i, token in enumerate(self.tokens):
            # (select の位置を特定
            if token.token_type == T.L_PAREN:
                next_token = self.tokens[i + 1] if i + 1 < len(self.tokens) else None
                if next_token and next_token.token_type == T.SELECT:
                    # サブクエリの開始位置を保持する
                    stack.append(token.start)
                else:
                    # サブクエリ以外で(があった場合、保持しない
                    stack.append(False)
            elif token.token_type == T.R_PAREN:
                if stack:
                    start = stack.pop()
                    # サブクエリであるかの判断
                    if start is not False:
                        ranges.append((start, token.end + 1))
        # クエリ全体をサブクエリとして扱う
        ranges.append((self.tokens[0].start, self.tokens[-1].end + 1))
        return sorted(ranges)

    def get_subquery_texts(self) -> list[str]:
        texts = []
        for start, end in self.subquery_ranges:
            texts.append(self.query[start:end])
        return texts

    def get_subquery_depths(self) -> list[int]:
        subquery_depths = []
        for target_start, target_end in self.subquery_ranges:
            depth = 0
            # 左に(があり、右に)がある場合、depthを増やす
            for search_start, search_end in self.subquery_ranges:
                if target_start > search_start and target_end < search_end:
                    depth += 1
            subquery_depths.append(depth)
        return subquery_depths
