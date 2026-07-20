from fastapi import APIRouter

from app.schemas.coach import CoachEchoRequest, CoachEchoResponse
from app.services.coach_echo_service import CoachEchoService

router = APIRouter()
echo_service = CoachEchoService()


@router.post("/echo", response_model=CoachEchoResponse)
async def echo(request: CoachEchoRequest) -> CoachEchoResponse:
    return echo_service.echo(request)
