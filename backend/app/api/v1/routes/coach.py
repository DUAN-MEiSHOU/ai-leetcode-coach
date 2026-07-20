from fastapi import APIRouter, HTTPException, status

from app.llm.errors import LLMConfigurationError, LLMError
from app.llm.factory import create_llm_provider
from app.schemas.coach import (
    CoachEchoRequest,
    CoachEchoResponse,
    CoachExplainRequest,
    CoachExplainResponse,
)
from app.services.coach_echo_service import CoachEchoService
from app.services.coach_explanation_service import CoachExplanationService

router = APIRouter()
echo_service = CoachEchoService()


@router.post("/echo", response_model=CoachEchoResponse)
async def echo(request: CoachEchoRequest) -> CoachEchoResponse:
    return echo_service.echo(request)


@router.post("/explain", response_model=CoachExplainResponse)
async def explain(request: CoachExplainRequest) -> CoachExplainResponse:
    service = CoachExplanationService(create_llm_provider())

    try:
        return await service.explain(request)
    except LLMConfigurationError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(error),
        ) from error
    except LLMError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The configured LLM provider returned an invalid response.",
        ) from error
