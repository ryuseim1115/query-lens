from fastapi import APIRouter, HTTPException
from api.db.run_subqueries import run_subqueries
from api.schemas.run_query import QueryInfo, SubqueryAnalyzeResultList
from api.services.analyze.query_structure_analyzer import QueryStructureAnalyzer
from api.validators.query_validator import QueryValidator

router = APIRouter()


@router.post("/run-query", response_model=SubqueryAnalyzeResultList)
def run_query(body: QueryInfo):
    try:
        QueryValidator(body.database_type, body.query).validate()
        subqueries = QueryStructureAnalyzer(body.query).execute()
        return run_subqueries(subqueries)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
