from app.llm.provider import LLMProvider
from app.llm.prompts.coach import PROMPT_VERSION, build_coaching_messages
from app.llm.types import LLMRequest
from app.schemas.coach import CoachExplainRequest, CoachExplainResponse
from app.services.python_code_analysis_service import PythonCodeAnalysisService


class CoachExplanationService:
    def __init__(
        self,
        llm_provider: LLMProvider,
        python_code_analysis_service: PythonCodeAnalysisService | None = None,
    ) -> None:
        self._llm_provider = llm_provider
        self._python_code_analysis_service = (
            python_code_analysis_service or PythonCodeAnalysisService()
        )

    async def explain(self, request: CoachExplainRequest) -> CoachExplainResponse:
        code_context = self._build_code_context(request)
        llm_response = await self._llm_provider.generate(
            LLMRequest(messages=build_coaching_messages(request, code_context))
        )

        return CoachExplainResponse(
            mode=request.mode,
            source=request.source,
            provider=llm_response.provider,
            model=llm_response.model,
            prompt_version=PROMPT_VERSION,
            code_context=code_context,
            explanation=llm_response.content,
        )

    def _build_code_context(self, request: CoachExplainRequest):
        if request.language not in {"auto", "python"}:
            return None

        code_context = self._python_code_analysis_service.analyze(
            request.surrounding_context or request.content,
            request.selected_line_number,
        )
        if request.language == "auto" and not code_context.syntax_valid:
            return None
        return code_context
