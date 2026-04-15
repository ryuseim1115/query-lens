from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.services.query_validator import QueryValidator
from api.services.analyze_subquery import AnalyzeSubquery

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/run-query")
def run_query(body: QueryRequest):
    database_type = "mysql"
    validator = QueryValidator(database_type, body.query)
    is_valid, error_msg = validator.validate_query()
    if not is_valid:
        raise HTTPException(status_code=400, detail=str(error_msg))
    try:
        subquery_analyzer = AnalyzeSubquery(body.query)
        query_information = []
        for query, depth in zip(
            subquery_analyzer.subquery_texts, subquery_analyzer.subquery_depths
        ):
            #   cursor.execute(query)
            #  query_result = cursor.fetchall()
            query_information.append(
                {"query": query, "depth": depth, "query_result": query_result}
            )
        return query_information
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
