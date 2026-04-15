from pydantic import BaseModel


class AnalyzeQueryBody(BaseModel):
    database_type: str
    query: str
