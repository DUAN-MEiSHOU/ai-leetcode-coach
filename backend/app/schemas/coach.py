from typing import Literal

from pydantic import BaseModel, Field


CoachMode = Literal[
    "manual",
    "explain_problem",
    "hint",
    "pseudocode",
    "complete_solution",
    "explain_code",
    "explain_line",
    "explain_syntax",
    "explain_library",
    "analyse_error",
]

InputSource = Literal["manual_paste", "page_selection"]


class CoachEchoRequest(BaseModel):
    mode: CoachMode = "manual"
    source: InputSource
    content: str = Field(min_length=1, max_length=20_000)


class CoachEchoResponse(BaseModel):
    status: Literal["ok"] = "ok"
    mode: CoachMode
    source: InputSource
    content_length: int
    message: str
