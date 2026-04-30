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


class JoinLinkRow(BaseModel):
    """「左テーブルのこの行 ↔ 右テーブルのこれらの行」を指す対応（矢印描画用）。"""

    left_row: int
    right_rows: list[int]


class JoinPreview(BaseModel):
    """JOIN 両側の実テーブルを並べて結合キー・行対応を可視化するためのデータ。"""

    left_title: str
    right_title: str
    left_columns: list[str]
    right_columns: list[str]
    left_join_columns: list[str]
    right_join_columns: list[str]
    left_rows: list[dict[str, Any]]
    right_rows: list[dict[str, Any]]
    links: list[JoinLinkRow]


class SubqueryAnalyzeResult(BaseModel):
    query: str
    depth: int
    start_index: int
    end_index: int
    joins: list[JoinInfo] = []
    join_previews: list[JoinPreview | None] = []
    tables: list[str] = []
    result: list[dict[str, Any]]
    error: str | None = None
    from_alias: str | None = None
    from_table: str | None = None
    from_subquery: str | None = None
    cte_name: str | None = None
    parent_alias: str | None = None


SubqueryAnalyzeResultList = list[SubqueryAnalyzeResult]


class RunQueryResponse(BaseModel):
    subqueries: list[SubqueryAnalyzeResult]
