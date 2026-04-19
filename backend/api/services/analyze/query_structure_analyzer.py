from api.schemas.run_query import SubqueryAnalyzeResult, SubqueryAnalyzeResultList
from api.services.analyze.analyze_subquery import AnalyzeSubquery


class QueryStructureAnalyzer:
    def __init__(self, query: str):
        self.query = query

    def execute(self) -> SubqueryAnalyzeResultList:
        analyzer = AnalyzeSubquery(self.query)
        return [
            SubqueryAnalyzeResult(query=query, depth=depth, result=[])
            for query, depth in zip(analyzer.subquery_texts, analyzer.subquery_depths)
        ]
