from fastapi import APIRouter, Request
from api.db_connector import DbConnector

router = APIRouter()


@router.post("/db_connector")
def db_connect(settings: dict, request: Request):
    connection = DbConnector(settings)
    is_connect, message = connection.connect()
    if is_connect:
        request.app.state.db_connector = connection
    return {"is_connect": is_connect, "message": message}
