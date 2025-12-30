"""Error handling middleware.

This module provides global error handling middleware.
"""

import traceback
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import get_settings
from src.core.exceptions import BaseDocxException


class ErrorMiddleware(BaseHTTPMiddleware):
    """Middleware for global error handling.

    This middleware catches unhandled exceptions and returns
    appropriate JSON error responses.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Process the request and handle errors.

        Args:
            request: Incoming request.
            call_next: Next middleware/handler.

        Returns:
            Response from the next handler or error response.
        """
        try:
            return await call_next(request)
        except BaseDocxException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=e.to_dict(),
            )
        except Exception as e:
            settings = get_settings()

            error_detail = {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            }

            if settings.debug:
                error_detail["message"] = str(e)
                error_detail["traceback"] = traceback.format_exc()

            return JSONResponse(
                status_code=500,
                content={"error": error_detail},
            )
