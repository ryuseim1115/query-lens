from dataclasses import dataclass, field
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


class AnalyzeSubquery:
    def __init__(self, query: str):
        self.query = query
        self._tokens = sqlglot.tokens.Tokenizer().tokenize(query)

    def execute(self) -> list[Subquery]:
        return self._build()

    def _build(self) -> list[Subquery]:
        ranges = find_subquery_ranges(self.query, self._tokens)
        cte_ranges = find_cte_ranges(self._tokens)
        queries = [self.query[start:end] for start, end in ranges]
        depths = get_subquery_depths(ranges)
        result = []
        for (start, end), query, depth in zip(ranges, queries, depths):
            joins = extract_joins(query)
            from_alias, from_table, from_subquery = extract_from_info(query)
            cte_name = cte_ranges.get((start, end))
            result.append(
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
        return result
