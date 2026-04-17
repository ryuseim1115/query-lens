from fastapi import APIRouter, HTTPException
from api.schemas.run_query import QueryInfo, SubqueryAnalyzeResultList
from api.services.run_query_service import RunQueryService

router = APIRouter()


@router.post("/run-query", response_model=SubqueryAnalyzeResultList)
def run_query(body: QueryInfo):
    try:
        service = RunQueryService(body.database_type, body.query)
        return service.execute()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
