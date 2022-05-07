from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from app.web.api.router import api_router
from app.web.lifetime import shutdown, startup
from importlib import metadata


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="task_service",
        description="",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    app.include_router(router=api_router, prefix="/api")

    return app
