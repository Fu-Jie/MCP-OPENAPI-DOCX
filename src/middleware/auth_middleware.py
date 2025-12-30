"""Authentication middleware.

This module provides authentication middleware for API requests.
"""

from typing import Callable

from fastapi import Request, Response
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import get_settings


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for JWT authentication.

    This middleware extracts and validates JWT tokens from requests,
    adding user information to the request state.
    """

    # Paths that don't require authentication
    PUBLIC_PATHS = {
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/health",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
    }

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        """Process the request and add user info.

        Args:
            request: Incoming request.
            call_next: Next middleware/handler.

        Returns:
            Response from the next handler.
        """
        # Skip authentication for public paths
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        # Also skip for paths starting with certain prefixes
        if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc"):
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        request.state.user = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            settings = get_settings()

            try:
                payload = jwt.decode(
                    token,
                    settings.secret_key,
                    algorithms=[settings.algorithm],
                )
                request.state.user = payload
            except JWTError:
                # Invalid token, but we don't block - let the route handle it
                pass

        return await call_next(request)
