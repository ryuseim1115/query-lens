from pydantic import BaseModel


class QueryInfo(BaseModel):
    database_type: str
    query: str


class SubqueryAnalyzeResult(BaseModel):
    query: str
    depth: int


SubqueryAnalyzeResultList = list[SubqueryAnalyzeResult]
