from api.schemas.run_query import SubqueryAnalyzeResult, SubqueryAnalyzeResultList
from api.services.query_validator import QueryValidator
from api.services.analyze_subquery import AnalyzeSubquery


class RunQueryService:
    def __init__(self, database_type: str, query: str):
        self.database_type = database_type
        self.query = query

    def execute(self) -> SubqueryAnalyzeResultList:
        self._validate()
        return self._analyze_subqueries()

    def _validate(self):
        QueryValidator(self.database_type, self.query).validate()

    def _analyze_subqueries(self) -> SubqueryAnalyzeResultList:
        analyzer = AnalyzeSubquery(self.query)
        return [
            SubqueryAnalyzeResult(query=query, depth=depth)
            for query, depth in zip(analyzer.subquery_texts, analyzer.subquery_depths)
        ]
