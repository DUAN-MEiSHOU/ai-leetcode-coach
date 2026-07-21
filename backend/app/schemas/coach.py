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
CoachLanguage = Literal["auto", "python"]


class SourceLine(BaseModel):
    number: int
    content: str


class PythonCodeContext(BaseModel):
    language: Literal["python"] = "python"
    syntax_valid: bool
    syntax_error: str | None = None
    imports: list[str] = Field(default_factory=list)
    function_calls: list[str] = Field(default_factory=list)
    standard_library_calls: list[str] = Field(default_factory=list)
    selected_line_number: int | None = None
    selected_line: str | None = None
    surrounding_lines: list[SourceLine] = Field(default_factory=list)


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


class CoachExplainRequest(BaseModel):
    mode: CoachMode
    source: InputSource
    content: str = Field(min_length=1, max_length=20_000)
    language: CoachLanguage = "auto"
    selected_line_number: int | None = Field(default=None, ge=1)
    surrounding_context: str | None = Field(default=None, max_length=20_000)


class CoachExplainResponse(BaseModel):
    status: Literal["ok"] = "ok"
    mode: CoachMode
    source: InputSource
    provider: str
    model: str
    prompt_version: str
    code_context: PythonCodeContext | None = None
    explanation: str
