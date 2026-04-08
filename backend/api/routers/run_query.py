from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.db_connector import DbConnector
from api.dependencies import get_db
from api.services.query_validator import QueryValidator
from api.services.analyze import analyze
from api.services.debug_sql_walk import SQLWalkDebugger

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/run-query")
def run_query(body: QueryRequest, db: DbConnector = Depends(get_db)):
    validator = QueryValidator(db.database_type, body.query)
    is_valid, error_msg = validator.validate_query()
    if not is_valid:
        raise HTTPException(status_code=400, detail=str(error_msg))
    cursor = db.connection.cursor(dictionary=True)
    try:
        cursor.execute(body.query)
        sql_result = cursor.fetchall()
        tables = analyze(body.query)
        debugger = SQLWalkDebugger(body.query)
        debugger.visualize()
        colored_sql = debugger.get_colored_html()

        return {"sql_result": sql_result, "tables": tables, "colored_sql": colored_sql}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
