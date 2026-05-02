from dataclasses import dataclass

import sqlglot
from api.services.analyze_subquery.subquery_depth_analyzer import get_subquery_depths
from api.services.analyze_subquery.subquery_range_finder import (
    find_cte_ranges,
    find_subquery_ranges,
)
from api.services.analyze_subquery.subquery_table_extractor import (
    extract_tables_with_alias,
)


@dataclass
class Subquery:
    start_index: int
    end_index: int
    query: str
    depth: int
    tables_name_alias: list[tuple[str | None, str | None]]
    parent_alias: str | None = None


class AnalyzeSubquery:
    def __init__(self, query: str):
        self.query = query
        self._tokens = sqlglot.tokens.Tokenizer().tokenize(query)

    def execute(self) -> list[Subquery]:
        return self._build()

    def _build(self) -> list[Subquery]:
        subquery_ranges_alias = find_subquery_ranges(self.query, self._tokens)
        cte_ranges_alias = find_cte_ranges(self._tokens)
        ranges = list(subquery_ranges_alias.keys())
        depths = get_subquery_depths(ranges)
        queries = [self.query[start:end] for start, end in ranges]
        subquery_tables_name_alias = [
            extract_tables_with_alias(query) for query in queries
        ]

        subqueries = []
        for (start, end), query, depth, tables_name_alias in zip(
            ranges, queries, depths, subquery_tables_name_alias
        ):
            subqueries.append(
                Subquery(
                    start_index=start,
                    end_index=end,
                    query=query,
                    depth=depth,
                    tables_name_alias=tables_name_alias,
                    parent_alias=cte_ranges_alias.get((start, end))
                    or subquery_ranges_alias.get((start, end)),
                )
            )

        return subqueries
