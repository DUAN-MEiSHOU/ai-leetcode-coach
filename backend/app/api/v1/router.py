from fastapi import APIRouter

from app.api.v1.routes.coach import router as coach_router

api_router = APIRouter()
api_router.include_router(coach_router, prefix="/coach", tags=["coach"])
