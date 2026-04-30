from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class QueryInfo(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
    )
    database_type: str
    query: str


class JoinInfo(BaseModel):
    left_alias: str
    right_alias: str
    join_type: str
    on: str | None = None
    left_table: str | None = None
    right_table: str | None = None
    left_subquery: str | None = None
    right_subquery: str | None = None


class SubqueryAnalyzeResult(BaseModel):
    query: str
    depth: int
    start_index: int
    end_index: int
    tables: list[str] = []
    result: list[dict[str, Any]]
    error: str | None = None
    parent_alias: str | None = None


SubqueryAnalyzeResultList = list[SubqueryAnalyzeResult]


class RunQueryResponse(BaseModel):
    subqueries: list[SubqueryAnalyzeResult]
