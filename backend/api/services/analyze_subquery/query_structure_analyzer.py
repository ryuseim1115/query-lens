from api.schemas.run_query import SubqueryAnalyzeResult, SubqueryAnalyzeResultList, TableInfo
from api.services.analyze_subquery.subquery_builder import AnalyzeSubquery


class QueryStructureAnalyzer:
    def __init__(self, query: str):
        self.query = query

    def execute(self) -> SubqueryAnalyzeResultList:
        subqueries = AnalyzeSubquery(self.query).execute()
        return [
            SubqueryAnalyzeResult(
                start_index=subquery.start_index,
                end_index=subquery.end_index,
                query=subquery.query,
                depth=subquery.depth,
                tables_name_alias=[TableInfo(name=name, alias=alias) for name, alias in subquery.tables_name_alias],
                parent_alias=subquery.parent_alias,
                result=[],
            )
            for subquery in subqueries
        ]
