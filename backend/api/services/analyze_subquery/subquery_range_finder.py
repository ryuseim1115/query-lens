import sqlglot


def find_subquery_ranges(query: str, tokens: list) -> list[tuple[int, int]]:
    if not tokens:
        return []
    ranges = []
    stack = []
    T = sqlglot.tokens.TokenType
    for i, token in enumerate(tokens):
        if token.token_type == T.L_PAREN:
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            if next_token and next_token.token_type == T.SELECT:
                stack.append(token.start)
            else:
                stack.append(False)
        elif token.token_type == T.R_PAREN:
            if stack:
                start = stack.pop()
                if start is not False:
                    ranges.append((start, token.end + 1))
    ranges.append((tokens[0].start, tokens[-1].end + 1))
    return sorted(ranges)


def find_cte_ranges(tokens: list) -> dict[tuple[int, int], str]:
    """CTE本体の位置→CTE名のマッピングを返す。"""
    T = sqlglot.tokens.TokenType
    cte_map: dict[tuple[int, int], str] = {}
    for i, token in enumerate(tokens):
        if token.token_type != T.L_PAREN:
            continue
        next_tok = tokens[i + 1] if i + 1 < len(tokens) else None
        if not (next_tok and next_tok.token_type == T.SELECT):
            continue
        # IDENTIFIER AS ( の並びを確認
        if i < 2:
            continue
        prev1 = tokens[i - 1]
        prev2 = tokens[i - 2]
        if prev1.text.upper() != 'AS':
            continue
        cte_name = prev2.text
        # 対応する R_PAREN を探す
        depth = 1
        for k in range(i + 1, len(tokens)):
            if tokens[k].token_type == T.L_PAREN:
                depth += 1
            elif tokens[k].token_type == T.R_PAREN:
                depth -= 1
                if depth == 0:
                    cte_map[(token.start, tokens[k].end + 1)] = cte_name
                    break
    return cte_map
