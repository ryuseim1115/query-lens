from fastapi import APIRouter, HTTPException
from api.schemas.run_query import QueryInfo, RunQueryResponse
from api.services.analyze_subquery.query_structure_analyzer import (
    QueryStructureAnalyzer,
)
from api.services.analyze_subquery.subquery_runner import SubqueryRunner
from api.services.analyze_subquery.sort_subquery import SortSubquery
from api.validators.query_validator import QueryValidator

router = APIRouter()


@router.post("/run-query", response_model=RunQueryResponse)
def run_query(body: QueryInfo):
    try:
        QueryValidator(body.database_type, body.query).validate()
        subqueries = QueryStructureAnalyzer(body.query).execute()
        subqueries = SortSubquery(subqueries).execute()
        subqueries = SubqueryRunner(subqueries).execute()
        return RunQueryResponse(subqueries=subqueries)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
