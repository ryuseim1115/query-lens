from fastapi import APIRouter, HTTPException
from api.schemas.run_query import AnalyzeQueryBody
from api.services.query_validator import QueryValidator
from api.services.analyze_subquery import AnalyzeSubquery

router = APIRouter()


@router.post("/run-query")
def run_query(body: AnalyzeQueryBody):
    validator = QueryValidator(body.database_type, body.query)
    is_valid = validator.is_valid
    error_msg = validator.error_msg
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
            query_information.append({"query": query, "depth": depth})
        return query_information
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
