from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.learning import AttemptCreateRequest, AttemptCreateResponse, DueReviewResponse
from app.services.learning_record_service import LearningRecordService

router = APIRouter()


@router.post("/attempts", response_model=AttemptCreateResponse, status_code=201)
def create_attempt(
    request: AttemptCreateRequest,
    session: Session = Depends(get_session),
) -> AttemptCreateResponse:
    return LearningRecordService(session).record_attempt(request)


@router.get("/reviews/due", response_model=list[DueReviewResponse])
def get_due_reviews(
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
) -> list[DueReviewResponse]:
    return LearningRecordService(session).list_due_reviews(limit)
