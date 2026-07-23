from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.app_version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_origin_regex=settings.allowed_origin_regex,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "ai-leetcode-coach-api"}

    app.include_router(api_router, prefix="/api/v1")

    dashboard_directory = Path(__file__).parent / "web"
    app.mount("/dashboard", StaticFiles(directory=dashboard_directory, html=True), name="dashboard")

    @app.get("/", include_in_schema=False)
    async def dashboard() -> RedirectResponse:
        return RedirectResponse(url="/dashboard/")

    return app


app = create_app()
