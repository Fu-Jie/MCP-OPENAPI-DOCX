"""Application configuration management using pydantic-settings.

This module provides centralized configuration management for the application,
loading settings from environment variables and .env files.
"""

from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        app_name: Name of the application.
        app_version: Version of the application.
        debug: Enable debug mode.
        environment: Deployment environment (development, staging, production).
        host: Server host address.
        port: Server port number.
        workers: Number of worker processes.
        reload: Enable auto-reload for development.
        database_url: Database connection URL.
        database_pool_size: Connection pool size.
        database_max_overflow: Maximum overflow connections.
        redis_url: Redis connection URL.
        redis_cache_ttl: Cache TTL in seconds.
        celery_broker_url: Celery broker URL.
        celery_result_backend: Celery result backend URL.
        secret_key: Secret key for JWT encoding.
        access_token_expire_minutes: Access token expiration time.
        refresh_token_expire_days: Refresh token expiration time.
        algorithm: JWT encoding algorithm.
        cors_origins: Allowed CORS origins.
        cors_allow_credentials: Allow credentials in CORS.
        cors_allow_methods: Allowed HTTP methods for CORS.
        cors_allow_headers: Allowed headers for CORS.
        upload_dir: Directory for uploaded files.
        export_dir: Directory for exported files.
        temp_dir: Temporary files directory.
        max_upload_size: Maximum upload file size in bytes.
        allowed_extensions: Allowed file extensions.
        log_level: Logging level.
        log_format: Log format (json or text).
        log_file: Log file path.
        sentry_dsn: Sentry DSN for error tracking.
        prometheus_enabled: Enable Prometheus metrics.
        prometheus_port: Prometheus metrics port.
        mcp_server_name: MCP server name.
        mcp_server_version: MCP server version.
        mcp_transport: MCP transport type.
        max_document_size: Maximum document size in bytes.
        max_concurrent_documents: Maximum concurrent document operations.
        document_timeout: Document operation timeout in seconds.
        encryption_key: Key for document encryption.
        api_key_header: Header name for API key.
        rate_limit_requests: Rate limit requests count.
        rate_limit_window: Rate limit window in seconds.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="MCP-OPENAPI-DOCX")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    environment: str = Field(default="development")

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    workers: int = Field(default=4, ge=1)
    reload: bool = Field(default=False)

    # Database
    database_url: str = Field(default="sqlite+aiosqlite:///./docx_db.sqlite")
    database_pool_size: int = Field(default=10, ge=1)
    database_max_overflow: int = Field(default=20, ge=0)

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_cache_ttl: int = Field(default=3600, ge=0)

    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/1")
    celery_result_backend: str = Field(default="redis://localhost:6379/2")

    # Authentication
    secret_key: str = Field(default="your-super-secret-key-change-in-production")
    access_token_expire_minutes: int = Field(default=30, ge=1)
    refresh_token_expire_days: int = Field(default=7, ge=1)
    algorithm: str = Field(default="HS256")

    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"]
    )
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default=["*"])
    cors_allow_headers: list[str] = Field(default=["*"])

    # File Storage
    upload_dir: str = Field(default="./uploads")
    export_dir: str = Field(default="./exports")
    temp_dir: str = Field(default="./temp")
    max_upload_size: int = Field(default=104857600)  # 100MB
    allowed_extensions: list[str] = Field(
        default=[".docx", ".doc", ".pdf", ".html", ".md"]
    )

    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")
    log_file: str = Field(default="./logs/app.log")

    # Monitoring
    sentry_dsn: str = Field(default="")
    prometheus_enabled: bool = Field(default=True)
    prometheus_port: int = Field(default=9090, ge=1, le=65535)

    # MCP Server
    mcp_server_name: str = Field(default="docx-mcp-server")
    mcp_server_version: str = Field(default="1.0.0")
    mcp_transport: str = Field(default="stdio")

    # Document Processing
    max_document_size: int = Field(default=52428800)  # 50MB
    max_concurrent_documents: int = Field(default=10, ge=1)
    document_timeout: int = Field(default=300, ge=1)

    # Security
    encryption_key: str = Field(default="your-encryption-key-32-chars-long")
    api_key_header: str = Field(default="X-API-Key")
    rate_limit_requests: int = Field(default=100, ge=1)
    rate_limit_window: int = Field(default=60, ge=1)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        """Parse CORS origins from string or list.

        Args:
            v: Input value (string or list).

        Returns:
            List of CORS origins.
        """
        if isinstance(v, str):
            # Try to parse as JSON list
            import json

            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # Treat as comma-separated list
                return [origin.strip() for origin in v.split(",")]
        return v

    @field_validator("allowed_extensions", mode="before")
    @classmethod
    def parse_extensions(cls, v: Any) -> list[str]:
        """Parse allowed extensions from string or list.

        Args:
            v: Input value (string or list).

        Returns:
            List of allowed extensions.
        """
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production environment.

        Returns:
            True if environment is production.
        """
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development environment.

        Returns:
            True if environment is development.
        """
        return self.environment.lower() == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings.

    Returns:
        Application settings instance.
    """
    return Settings()
