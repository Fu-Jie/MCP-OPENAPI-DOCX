"""Cache utility functions.

This module provides caching utilities for improving
performance of document operations.
"""

import json
import hashlib
import asyncio
from typing import Any, Callable, TypeVar
from functools import wraps
from datetime import datetime, timedelta

T = TypeVar("T")


class InMemoryCache:
    """Simple in-memory cache implementation.

    Attributes:
        _cache: Dictionary storing cached values.
        _expiry: Dictionary storing expiration times.
        _default_ttl: Default time-to-live in seconds.
    """

    def __init__(self, default_ttl: int = 3600) -> None:
        """Initialize the cache.

        Args:
            default_ttl: Default TTL in seconds.
        """
        self._cache: dict[str, Any] = {}
        self._expiry: dict[str, datetime] = {}
        self._default_ttl = default_ttl

    def get(self, key: str) -> Any | None:
        """Get a cached value.

        Args:
            key: Cache key.

        Returns:
            Cached value or None.
        """
        if key not in self._cache:
            return None

        if key in self._expiry and datetime.utcnow() > self._expiry[key]:
            self.delete(key)
            return None

        return self._cache[key]

    def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        """Set a cached value.

        Args:
            key: Cache key.
            value: Value to cache.
            ttl: Time-to-live in seconds.
        """
        self._cache[key] = value
        if ttl or self._default_ttl:
            expiry_seconds = ttl or self._default_ttl
            self._expiry[key] = datetime.utcnow() + timedelta(seconds=expiry_seconds)

    def delete(self, key: str) -> bool:
        """Delete a cached value.

        Args:
            key: Cache key.

        Returns:
            True if deleted.
        """
        if key in self._cache:
            del self._cache[key]
            if key in self._expiry:
                del self._expiry[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self._expiry.clear()

    def exists(self, key: str) -> bool:
        """Check if key exists.

        Args:
            key: Cache key.

        Returns:
            True if key exists and not expired.
        """
        return self.get(key) is not None

    def keys(self) -> list[str]:
        """Get all cache keys.

        Returns:
            List of keys.
        """
        # Clean up expired keys
        now = datetime.utcnow()
        expired = [k for k, exp in self._expiry.items() if now > exp]
        for key in expired:
            self.delete(key)
        return list(self._cache.keys())


# Global cache instance
_cache = InMemoryCache()


def get_cache() -> InMemoryCache:
    """Get the global cache instance.

    Returns:
        Cache instance.
    """
    return _cache


def cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate a cache key from arguments.

    Args:
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Returns:
        Cache key string.
    """
    key_data = json.dumps(
        {"args": [str(a) for a in args], "kwargs": {str(k): str(v) for k, v in kwargs.items()}},
        sort_keys=True,
    )
    return hashlib.md5(key_data.encode()).hexdigest()


def cached(ttl: int = 3600) -> Callable:
    """Decorator for caching function results.

    Args:
        ttl: Time-to-live in seconds.

    Returns:
        Decorator function.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            cached_value = _cache.get(key)
            if cached_value is not None:
                return cached_value
            result = func(*args, **kwargs)
            _cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator


def async_cached(ttl: int = 3600) -> Callable:
    """Decorator for caching async function results.

    Args:
        ttl: Time-to-live in seconds.

    Returns:
        Decorator function.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            cached_value = _cache.get(key)
            if cached_value is not None:
                return cached_value
            result = await func(*args, **kwargs)
            _cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator


def invalidate_cache(pattern: str | None = None) -> int:
    """Invalidate cache entries.

    Args:
        pattern: Optional key pattern to match.

    Returns:
        Number of entries invalidated.
    """
    if pattern is None:
        count = len(_cache.keys())
        _cache.clear()
        return count

    count = 0
    for key in list(_cache.keys()):
        if pattern in key:
            _cache.delete(key)
            count += 1
    return count
