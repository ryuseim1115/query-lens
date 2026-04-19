from api.db.connection import get_connection
from api.schemas.run_query import SubqueryAnalyzeResult, SubqueryAnalyzeResultList


def run_subqueries(subqueries: SubqueryAnalyzeResultList) -> SubqueryAnalyzeResultList:
    con = get_connection()
    results = []
    for item in subqueries:
        try:
            rel = con.sql(item.query)
            rows = [dict(zip(rel.columns, row)) for row in rel.fetchall()]
            results.append(SubqueryAnalyzeResult(query=item.query, depth=item.depth, result=rows))
        except Exception as e:
            results.append(SubqueryAnalyzeResult(query=item.query, depth=item.depth, result=[], error=str(e)))
    return results
