from app.llm.provider import LLMProvider
from app.llm.types import LLMMessage, LLMRequest
from app.schemas.coach import CoachExplainRequest, CoachExplainResponse


class CoachExplanationService:
    def __init__(self, llm_provider: LLMProvider) -> None:
        self._llm_provider = llm_provider

    async def explain(self, request: CoachExplainRequest) -> CoachExplainResponse:
        llm_response = await self._llm_provider.generate(
            LLMRequest(
                messages=[
                    LLMMessage(
                        role="system",
                        content=(
                            "You are an educational algorithm coach. Explain clearly, "
                            "avoid pretending to run code, and keep copyrighted problem "
                            "text ephemeral."
                        ),
                    ),
                    LLMMessage(
                        role="user",
                        content=(
                            f"Mode: {request.mode}\n"
                            f"Source: {request.source}\n"
                            f"Language: {request.language or 'unspecified'}\n\n"
                            f"Content:\n{request.content}"
                        ),
                    ),
                ]
            )
        )

        return CoachExplainResponse(
            mode=request.mode,
            source=request.source,
            provider=llm_response.provider,
            model=llm_response.model,
            explanation=llm_response.content,
        )
