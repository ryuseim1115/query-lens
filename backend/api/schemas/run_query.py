from typing import Any
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
    result: list[dict[str, Any]]
    error: str | None = None


SubqueryAnalyzeResultList = list[SubqueryAnalyzeResult]
