from api.schemas.run_query import SubqueryAnalyzeResultList


class SortSubqueryByDepthDesc:
    def __init__(self, subqueries: SubqueryAnalyzeResultList):
        self.subqueries = subqueries

    def execute(self) -> SubqueryAnalyzeResultList:
        sorted_subquery = sorted(self.subqueries, key=lambda s: s.depth, reverse=True)
        return sorted_subquery
