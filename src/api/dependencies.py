"""Dependency injection for FastAPI routes.

This module defines all dependencies used across API routes
including database sessions, current user, and document handlers.
"""

from collections.abc import AsyncGenerator
from typing import Annotated, Any

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import Settings, get_settings
from src.core.enums import UserRole
from src.core.exceptions import AuthenticationError, PermissionDeniedError
from src.database.session import get_db
from src.handlers.document_handler import DocumentHandler
from src.models.dto import UserDTO


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency.

    Yields:
        AsyncSession for database operations.
    """
    async for session in get_db():
        yield session


def get_document_handler() -> DocumentHandler:
    """Get a document handler instance.

    Returns:
        DocumentHandler instance.
    """
    return DocumentHandler()


async def get_current_user_optional(
    authorization: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> UserDTO | None:
    """Get current user from JWT token (optional).

    Args:
        authorization: Authorization header value.
        settings: Application settings.

    Returns:
        UserDTO if authenticated, None otherwise.
    """
    if not authorization:
        return None

    if not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        user_id = payload.get("sub")
        if user_id is None:
            return None

        return UserDTO(
            id=int(user_id),
            uuid=payload.get("uuid", ""),
            email=payload.get("email", ""),
            username=payload.get("username", ""),
            role=UserRole(payload.get("role", "viewer")),
        )
    except JWTError:
        return None


async def get_current_user(
    authorization: str = Header(...),
    settings: Settings = Depends(get_settings),
) -> UserDTO:
    """Get current authenticated user from JWT token.

    Args:
        authorization: Authorization header value.
        settings: Application settings.

    Returns:
        UserDTO for the authenticated user.

    Raises:
        AuthenticationError: If authentication fails.
    """
    if not authorization.startswith("Bearer "):
        raise AuthenticationError("Invalid authorization header")

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthenticationError("Invalid token")

        return UserDTO(
            id=int(user_id),
            uuid=payload.get("uuid", ""),
            email=payload.get("email", ""),
            username=payload.get("username", ""),
            role=UserRole(payload.get("role", "viewer")),
        )
    except JWTError as e:
        raise AuthenticationError(f"Token validation failed: {e}")


def require_roles(*roles: UserRole):
    """Create a dependency that requires specific user roles.

    Args:
        *roles: Required roles (user must have one of these).

    Returns:
        Dependency function.
    """
    async def role_checker(
        current_user: UserDTO = Depends(get_current_user),
    ) -> UserDTO:
        if current_user.role not in roles:
            raise PermissionDeniedError(
                f"Required roles: {', '.join(r.value for r in roles)}"
            )
        return current_user

    return role_checker


# Type aliases for common dependencies
DBSession = Annotated[AsyncSession, Depends(get_db_session)]
CurrentUser = Annotated[UserDTO, Depends(get_current_user)]
CurrentUserOptional = Annotated[UserDTO | None, Depends(get_current_user_optional)]
DocHandler = Annotated[DocumentHandler, Depends(get_document_handler)]
AppSettings = Annotated[Settings, Depends(get_settings)]

# Role-based dependencies
AdminUser = Annotated[UserDTO, Depends(require_roles(UserRole.ADMIN))]
EditorUser = Annotated[
    UserDTO,
    Depends(require_roles(UserRole.ADMIN, UserRole.EDITOR)),
]
ReviewerUser = Annotated[
    UserDTO,
    Depends(require_roles(UserRole.ADMIN, UserRole.EDITOR, UserRole.REVIEWER)),
]
