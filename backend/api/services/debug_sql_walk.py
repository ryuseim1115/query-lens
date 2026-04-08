import sqlglot
from html import escape
from graphviz import Digraph
from datetime import datetime
from sqlglot.optimizer.scope import build_scope, ScopeType


class SQLWalkDebugger:
    def __init__(self, query, title="SQL AST Walk Analysis"):
        self.query = query
        self.parsed = sqlglot.parse_one(query)
        self.dot = Digraph(comment=title)
        self.node_ids = {}  # ノードオブジェクトをキーにしてIDを保持
        self.counter = 0

    def visualize(self, format="png", cleanup=True):
        """テーブルノードを描画してファイル出力する"""

        root_scope = build_scope(self.parsed)
        # ファイル名の生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"tmp/debug_walk_{timestamp}"

        self.dot.render(filename, format=format, cleanup=cleanup, view=False)

    def get_colored_html(self) -> str:
        """サブクエリブロック全体を深さに応じた背景色で色付けしたHTMLを返す"""

        # (SELECT ...) を検出して開始、終了位置を返す
        def find_subquery_ranges() -> list[tuple[int, int]]:
            tokens = sqlglot.tokens.Tokenizer().tokenize(self.query)
            subquery_ranges = []
            stack = []  # (の開始位置を保持する（サブクエリでなければ False）
            T = sqlglot.tokens.TokenType
            for i, token in enumerate(tokens):
                # (select の位置を特定
                if token.token_type == T.L_PAREN:
                    next_tokn = tokens[i + 1] if i + 1 < len(tokens) else None
                    if next_tokn and next_tokn.token_type == T.SELECT:
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
                            subquery_ranges.append((start, token.end + 1))
            return sorted(subquery_ranges)

        subquery_ranges = find_subquery_ranges()
        if not subquery_ranges:
            return f'<pre style="margin:0; white-space:pre-wrap;">{escape(self.query)}</pre>'

        # 探索対象よりも外側にあるサブクエリの数をカウントすることで深さを求める
        def subquery_depth(start: int, end: int) -> int:
            return sum(1 for s, e in subquery_ranges if s < start and end < e)

        # 深さに応じた背景色: 浅→薄青, 深→濃青
        BG_COLORS = [
            "rgba(116,185,255,0.25)",
            "rgba(9,132,227,0.25)",
            "rgba(6,82,221,0.25)",
            "rgba(30,55,153,0.25)",
            "rgba(12,36,97,0.30)",
        ]

        # 開始・終了イベントを位置順に並べて HTML を構築
        events: list[tuple[int, str]] = []

        for start, end in subquery_ranges:
            depth = subquery_depth(start, end)
            bg = BG_COLORS[min(depth, len(BG_COLORS) - 1)]
            events.append(
                (start, f'<span style="background:{bg}; border-radius:3px;">')
            )
            events.append((end, "</span>"))

        events.sort(key=lambda x: (x[0], 0 if x[1].startswith("</") else 1))

        pieces = []
        pos = 0
        for ev_pos, tag in events:
            if ev_pos > pos:
                pieces.append(escape(self.query[pos:ev_pos]))
            pieces.append(tag)
            pos = ev_pos

        pieces.append(escape(self.query[pos:]))
        return f'<pre style="margin:0; white-space:pre-wrap;">{"".join(pieces)}</pre>'
