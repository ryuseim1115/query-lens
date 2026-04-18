from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class QueryInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    database_type: str
    query: str


class SubqueryAnalyzeResult(BaseModel):
    query: str
    depth: int


SubqueryAnalyzeResultList = list[SubqueryAnalyzeResult]
