from dataclasses import dataclass
from typing import Literal


LLMRole = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class LLMMessage:
    role: LLMRole
    content: str


@dataclass(frozen=True)
class LLMRequest:
    messages: list[LLMMessage]
    temperature: float = 0.2


@dataclass(frozen=True)
class LLMResponse:
    content: str
    model: str
    provider: str
