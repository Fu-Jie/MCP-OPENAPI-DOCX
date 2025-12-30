"""Security routes.

This module provides endpoints for authentication and authorization.
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from src.api.dependencies import CurrentUser
from src.core.config import Settings, get_settings
from src.models.schemas import TokenResponse, UserCreate, UserLogin

router = APIRouter(prefix="/auth")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Simple in-memory user storage (would use database in production)
_users: dict[str, dict[str, Any]] = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(
    data: dict[str, Any],
    settings: Settings,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(
    data: dict[str, Any],
    settings: Settings,
) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register User",
    description="Register a new user account.",
)
async def register(
    data: UserCreate,
    settings: Settings = Depends(get_settings),
) -> dict[str, Any]:
    """Register a new user.

    Args:
        data: User registration data.
        settings: Application settings.

    Returns:
        Created user information.
    """
    if data.email in _users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    import uuid

    user_id = str(uuid.uuid4())

    user = {
        "id": len(_users) + 1,
        "uuid": user_id,
        "email": data.email,
        "username": data.username,
        "hashed_password": get_password_hash(data.password),
        "role": data.role.value,
        "is_active": True,
        "is_verified": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    _users[data.email] = user

    return {
        "uuid": user_id,
        "email": data.email,
        "username": data.username,
        "role": data.role.value,
    }


@router.post(
    "/login",
    summary="Login",
    description="Authenticate and get access token.",
)
async def login(
    data: UserLogin,
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    """Login and get tokens.

    Args:
        data: Login credentials.
        settings: Application settings.

    Returns:
        Access and refresh tokens.
    """
    user = _users.get(data.email)

    if not user or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    token_data = {
        "sub": str(user["id"]),
        "uuid": user["uuid"],
        "email": user["email"],
        "username": user["username"],
        "role": user["role"],
    }

    access_token = create_access_token(token_data, settings)
    refresh_token = create_refresh_token(token_data, settings)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.post(
    "/refresh",
    summary="Refresh Token",
    description="Refresh access token using refresh token.",
)
async def refresh_token(
    refresh_token: str,
    settings: Settings = Depends(get_settings),
) -> TokenResponse:
    """Refresh access token.

    Args:
        refresh_token: Refresh token.
        settings: Application settings.

    Returns:
        New access token.
    """
    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        token_data = {
            "sub": payload["sub"],
            "uuid": payload["uuid"],
            "email": payload["email"],
            "username": payload["username"],
            "role": payload["role"],
        }

        access_token = create_access_token(token_data, settings)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.access_token_expire_minutes * 60,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid refresh token: {e}",
        )


@router.get(
    "/me",
    summary="Get Current User",
    description="Get the currently authenticated user.",
)
async def get_current_user_info(current_user: CurrentUser) -> dict[str, Any]:
    """Get current user info.

    Args:
        current_user: Current authenticated user.

    Returns:
        User information.
    """
    return {
        "id": current_user.id,
        "uuid": current_user.uuid,
        "email": current_user.email,
        "username": current_user.username,
        "role": current_user.role.value,
    }


@router.post(
    "/logout",
    summary="Logout",
    description="Logout and invalidate tokens.",
)
async def logout() -> dict[str, bool]:
    """Logout user.

    Returns:
        Logout confirmation.
    """
    # In production, would invalidate the token
    return {"logged_out": True}


@router.post(
    "/change-password",
    summary="Change Password",
    description="Change the current user's password.",
)
async def change_password(
    current_password: str,
    new_password: str,
    current_user: CurrentUser,
) -> dict[str, bool]:
    """Change password.

    Args:
        current_password: Current password.
        new_password: New password.
        current_user: Current authenticated user.

    Returns:
        Confirmation.
    """
    user = None
    for u in _users.values():
        if u["id"] == current_user.id:
            user = u
            break

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not verify_password(current_password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    user["hashed_password"] = get_password_hash(new_password)

    return {"password_changed": True}
