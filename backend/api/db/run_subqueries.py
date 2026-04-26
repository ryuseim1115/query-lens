from api.db.connection import get_connection
from api.schemas.run_query import SubqueryAnalyzeResultList


def run_subqueries(subqueries: SubqueryAnalyzeResultList) -> SubqueryAnalyzeResultList:
    con = get_connection()
    for subquery in subqueries:
        try:
            result = con.sql(subquery.query)
            subquery.result = [dict(zip(result.columns, record)) for record in result.fetchall()]
        except Exception as e:
            subquery.error = str(e)
    return subqueries
