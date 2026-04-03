from fastapi import Request, HTTPException
from api.db_connector import DbConnector


def get_db(request: Request) -> DbConnector:
    db = getattr(request.app.state, "db_connector", None)
    if db is None:
        raise HTTPException(status_code=400, detail="DB未接続")
    return db
