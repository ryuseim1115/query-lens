from api.schemas.run_query import SubqueryAnalyzeResult, SubqueryAnalyzeResultList
from api.services.analyze_subquery.analyze_subquery import AnalyzeSubquery


class QueryStructureAnalyzer:
    def __init__(self, query: str):
        self.query = query

    def execute(self) -> SubqueryAnalyzeResultList:
        subqueries = AnalyzeSubquery(self.query).execute()
        return [
            SubqueryAnalyzeResult(
                query=subquery.query,
                depth=subquery.depth,
                start_index=subquery.start_index,
                end_index=subquery.end_index,
                parent_alias=subquery.parent_alias,
                tables=(
                    ([subquery.from_table] if subquery.from_table else ([subquery.from_alias] if subquery.from_alias else []))
                    + [j.right_table if j.right_table else j.right_alias for j in subquery.joins if j.right_table or j.right_alias]
                ),
                result=[],
            )
            for subquery in subqueries
        ]
