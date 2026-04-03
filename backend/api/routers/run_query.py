from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.db_connector import DbConnector
from api.dependencies import get_db
from api.services.analyze import analyze

router = APIRouter()


class QueryRequest(BaseModel):
    query: str


@router.post("/run-query")
def run_query(body: QueryRequest, db: DbConnector = Depends(get_db)):
    cursor = db.connection.cursor(dictionary=True)
    try:
        cursor.execute(body.query)
        sql_result = cursor.fetchall()
        tables = analyze(body.query)
        return {"sql_result": sql_result, "tables": tables}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
