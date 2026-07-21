from app.llm.provider import LLMProvider
from app.llm.prompts.coach import PROMPT_VERSION, build_coaching_messages
from app.llm.types import LLMRequest
from app.schemas.coach import CoachExplainRequest, CoachExplainResponse


class CoachExplanationService:
    def __init__(self, llm_provider: LLMProvider) -> None:
        self._llm_provider = llm_provider

    async def explain(self, request: CoachExplainRequest) -> CoachExplainResponse:
        llm_response = await self._llm_provider.generate(
            LLMRequest(messages=build_coaching_messages(request))
        )

        return CoachExplainResponse(
            mode=request.mode,
            source=request.source,
            provider=llm_response.provider,
            model=llm_response.model,
            prompt_version=PROMPT_VERSION,
            explanation=llm_response.content,
        )
