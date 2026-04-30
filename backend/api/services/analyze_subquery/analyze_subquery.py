from dataclasses import dataclass
import sqlglot

from api.schemas.run_query import JoinInfo
from api.services.analyze_subquery.subquery_range_finder import (
    find_subquery_ranges,
    find_cte_ranges,
)
from api.services.analyze_subquery.subquery_depth_analyzer import get_subquery_depths
from api.services.analyze_subquery.analyze_join import extract_joins, extract_from_info


@dataclass
class Subquery:
    start_index: int
    end_index: int
    query: str
    depth: int
    joins: list[JoinInfo]
    from_alias: str | None = None
    from_table: str | None = None
    from_subquery: str | None = None
    cte_name: str | None = None
    parent_alias: str | None = None


class AnalyzeSubquery:
    def __init__(self, query: str):
        self.query = query
        self._tokens = sqlglot.tokens.Tokenizer().tokenize(query)

    def execute(self) -> list[Subquery]:
        return self._build()

    def _build(self) -> list[Subquery]:
        ranges = find_subquery_ranges(self.query, self._tokens)
        depths = get_subquery_depths(ranges)
        queries = [self.query[start:end] for start, end in ranges]
        cte_ranges = find_cte_ranges(self._tokens)

        subqueries = []
        for (start, end), query, depth in zip(ranges, queries, depths):
            joins = extract_joins(query)
            from_alias, from_table, from_subquery = extract_from_info(query)
            cte_name = cte_ranges.get((start, end))
            subqueries.append(
                Subquery(
                    start_index=start,
                    end_index=end,
                    query=query,
                    depth=depth,
                    joins=joins,
                    from_alias=from_alias,
                    from_table=from_table,
                    from_subquery=from_subquery,
                    cte_name=cte_name,
                )
            )
        subqueries = self._find_parent_start_index(subqueries)

        return subqueries

    @staticmethod
    def _sqlglot_normalize(sql: str) -> str | None:
        s = sql.strip()
        if s.startswith("(") and s.endswith(")"):
            s = s[1:-1].strip()
        try:
            return sqlglot.parse_one(s).sql()
        except Exception:
            return None

    def _find_parent_start_index(self, subqueries: list[Subquery]) -> list[Subquery]:
        subqueries = sorted(subqueries, key=lambda s: s.start_index)
        for target_index in range(len(subqueries)):
            for search_index in range(target_index - 1, -2, -1):
                if search_index == -1:
                    break
                if subqueries[target_index].depth - 1 == subqueries[search_index].depth:
                    child = subqueries[target_index]
                    parent = subqueries[search_index]
                    child.parent_alias = (
                        child.cte_name
                        if child.cte_name
                        else self._resolve_parent_alias(child, parent)
                    )
                    break
        return subqueries

    @staticmethod
    def _resolve_parent_alias(child: Subquery, parent: Subquery) -> str | None:
        child = AnalyzeSubquery._sqlglot_normalize(child.query)
        if (
            parent.from_subquery
            and AnalyzeSubquery._sqlglot_normalize(parent.from_subquery) == child
        ):
            return parent.from_alias
        for join in parent.joins:
            if (
                join.left_subquery
                and AnalyzeSubquery._sqlglot_normalize(join.left_subquery) == child
            ):
                return join.left_alias
            if (
                join.right_subquery
                and AnalyzeSubquery._sqlglot_normalize(join.right_subquery) == child
            ):
                return join.right_alias
        return None
