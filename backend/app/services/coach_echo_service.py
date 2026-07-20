from app.schemas.coach import CoachEchoRequest, CoachEchoResponse


class CoachEchoService:
    def echo(self, request: CoachEchoRequest) -> CoachEchoResponse:
        return CoachEchoResponse(
            mode=request.mode,
            source=request.source,
            content_length=len(request.content),
            message=(
                "Backend echo received the coach request. DeepSeek, persistence, "
                "and review scheduling are not connected yet."
            ),
        )
