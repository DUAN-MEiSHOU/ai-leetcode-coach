from fastapi import APIRouter

from app.api.v1.routes.learning import router as learning_router

from app.api.v1.routes.coach import router as coach_router

api_router = APIRouter()
api_router.include_router(learning_router)
api_router.include_router(coach_router, prefix="/coach", tags=["coach"])
