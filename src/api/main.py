"""FastAPI application main entry point.

This module creates and configures the FastAPI application instance
with all middleware, routes, and error handlers.
"""

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.config import get_settings
from src.core.constants import (
    API_V1_PREFIX,
    OPENAPI_DESCRIPTION,
    OPENAPI_TITLE,
    OPENAPI_VERSION,
)
from src.core.exceptions import BaseDocxException

# Import routes
from src.api.routes import (
    documents,
    text,
    tables,
    lists,
    media,
    styles,
    layout,
    toc,
    comments,
    revisions,
    search,
    export,
    templates,
    security,
    metadata,
    batch,
    health,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Args:
        app: FastAPI application instance.

    Yields:
        None after startup, cleanup on shutdown.
    """
    # Startup
    settings = get_settings()
    app.state.start_time = time.time()

    # Create directories if they don't exist
    import os
    for dir_path in [settings.upload_dir, settings.export_dir, settings.temp_dir]:
        os.makedirs(dir_path, exist_ok=True)

    yield

    # Shutdown
    from src.database.base import dispose_engine
    await dispose_engine()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=OPENAPI_TITLE,
        description=OPENAPI_DESCRIPTION,
        version=OPENAPI_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # Add custom exception handlers
    @app.exception_handler(BaseDocxException)
    async def docx_exception_handler(
        request: Request,
        exc: BaseDocxException,
    ) -> JSONResponse:
        """Handle custom application exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle unexpected exceptions."""
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(exc) if settings.debug else "Internal server error",
                }
            },
        )

    # Request timing middleware
    @app.middleware("http")
    async def add_process_time_header(
        request: Request,
        call_next,
    ) -> Response:
        """Add processing time header to responses."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # Include API routes
    app.include_router(health.router, prefix=API_V1_PREFIX, tags=["Health"])
    app.include_router(documents.router, prefix=API_V1_PREFIX, tags=["Documents"])
    app.include_router(text.router, prefix=API_V1_PREFIX, tags=["Text"])
    app.include_router(tables.router, prefix=API_V1_PREFIX, tags=["Tables"])
    app.include_router(lists.router, prefix=API_V1_PREFIX, tags=["Lists"])
    app.include_router(media.router, prefix=API_V1_PREFIX, tags=["Media"])
    app.include_router(styles.router, prefix=API_V1_PREFIX, tags=["Styles"])
    app.include_router(layout.router, prefix=API_V1_PREFIX, tags=["Layout"])
    app.include_router(toc.router, prefix=API_V1_PREFIX, tags=["TOC"])
    app.include_router(comments.router, prefix=API_V1_PREFIX, tags=["Comments"])
    app.include_router(revisions.router, prefix=API_V1_PREFIX, tags=["Revisions"])
    app.include_router(search.router, prefix=API_V1_PREFIX, tags=["Search"])
    app.include_router(export.router, prefix=API_V1_PREFIX, tags=["Export"])
    app.include_router(templates.router, prefix=API_V1_PREFIX, tags=["Templates"])
    app.include_router(security.router, prefix=API_V1_PREFIX, tags=["Security"])
    app.include_router(metadata.router, prefix=API_V1_PREFIX, tags=["Metadata"])
    app.include_router(batch.router, prefix=API_V1_PREFIX, tags=["Batch"])

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root() -> dict[str, Any]:
        """Root endpoint with API information."""
        return {
            "name": OPENAPI_TITLE,
            "version": OPENAPI_VERSION,
            "docs": "/docs",
            "openapi": "/openapi.json",
        }

    return app


# Create application instance
app = create_application()


def run() -> None:
    """Run the application with uvicorn."""
    settings = get_settings()
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        workers=settings.workers if not settings.reload else 1,
    )


if __name__ == "__main__":
    run()
