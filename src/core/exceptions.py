"""Custom exception classes for the application.

This module defines all custom exceptions used throughout the application,
providing consistent error handling and messaging.
"""

from typing import Any


class BaseDocxException(Exception):
    """Base exception for all application exceptions.

    Attributes:
        message: Human-readable error message.
        code: Error code for API responses.
        status_code: HTTP status code.
        details: Additional error details.
    """

    def __init__(
        self,
        message: str = "An error occurred",
        code: str = "ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            code: Error code for API responses.
            status_code: HTTP status code.
            details: Additional error details.
        """
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API responses.

        Returns:
            Dictionary representation of the exception.
        """
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }


class DocumentNotFoundError(BaseDocxException):
    """Exception raised when a document is not found.

    Attributes:
        document_id: ID of the document that was not found.
    """

    def __init__(
        self,
        document_id: str | int | None = None,
        message: str = "Document not found",
    ) -> None:
        """Initialize the exception.

        Args:
            document_id: ID of the document that was not found.
            message: Human-readable error message.
        """
        details = {"document_id": document_id} if document_id else {}
        super().__init__(
            message=message,
            code="DOCUMENT_NOT_FOUND",
            status_code=404,
            details=details,
        )
        self.document_id = document_id


class TemplateNotFoundError(BaseDocxException):
    """Exception raised when a template is not found.

    Attributes:
        template_id: ID of the template that was not found.
    """

    def __init__(
        self,
        template_id: str | int | None = None,
        message: str = "Template not found",
    ) -> None:
        """Initialize the exception.

        Args:
            template_id: ID of the template that was not found.
            message: Human-readable error message.
        """
        details = {"template_id": template_id} if template_id else {}
        super().__init__(
            message=message,
            code="TEMPLATE_NOT_FOUND",
            status_code=404,
            details=details,
        )
        self.template_id = template_id


class InvalidDocumentError(BaseDocxException):
    """Exception raised when a document is invalid or corrupted."""

    def __init__(
        self,
        message: str = "Invalid document format",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="INVALID_DOCUMENT",
            status_code=400,
            details=details or {},
        )


class DocumentProcessingError(BaseDocxException):
    """Exception raised when document processing fails."""

    def __init__(
        self,
        message: str = "Document processing failed",
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            details: Additional error details.
        """
        super().__init__(
            message=message,
            code="DOCUMENT_PROCESSING_ERROR",
            status_code=500,
            details=details or {},
        )


class PermissionDeniedError(BaseDocxException):
    """Exception raised when user lacks required permissions."""

    def __init__(
        self,
        message: str = "Permission denied",
        required_permission: str | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            required_permission: The permission that was required.
        """
        details = (
            {"required_permission": required_permission} if required_permission else {}
        )
        super().__init__(
            message=message,
            code="PERMISSION_DENIED",
            status_code=403,
            details=details,
        )


class ValidationError(BaseDocxException):
    """Exception raised when validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            errors: List of validation errors.
        """
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details={"errors": errors or []},
        )
        self.errors = errors or []


class AuthenticationError(BaseDocxException):
    """Exception raised when authentication fails."""

    def __init__(
        self,
        message: str = "Authentication required",
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
        """
        super().__init__(
            message=message,
            code="AUTHENTICATION_REQUIRED",
            status_code=401,
        )


class TokenExpiredError(BaseDocxException):
    """Exception raised when a token has expired."""

    def __init__(
        self,
        message: str = "Token has expired",
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
        """
        super().__init__(
            message=message,
            code="TOKEN_EXPIRED",
            status_code=401,
        )


class InvalidTokenError(BaseDocxException):
    """Exception raised when a token is invalid."""

    def __init__(
        self,
        message: str = "Invalid token",
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
        """
        super().__init__(
            message=message,
            code="INVALID_TOKEN",
            status_code=401,
        )


class RateLimitExceededError(BaseDocxException):
    """Exception raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            retry_after: Seconds until rate limit resets.
        """
        details = {"retry_after": retry_after} if retry_after else {}
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=details,
        )


class FileTooLargeError(BaseDocxException):
    """Exception raised when a file exceeds the size limit."""

    def __init__(
        self,
        message: str = "File size exceeds maximum limit",
        max_size: int | None = None,
        actual_size: int | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            max_size: Maximum allowed file size in bytes.
            actual_size: Actual file size in bytes.
        """
        details: dict[str, Any] = {}
        if max_size:
            details["max_size"] = max_size
        if actual_size:
            details["actual_size"] = actual_size
        super().__init__(
            message=message,
            code="FILE_TOO_LARGE",
            status_code=413,
            details=details,
        )


class UnsupportedFormatError(BaseDocxException):
    """Exception raised when a file format is not supported."""

    def __init__(
        self,
        message: str = "Unsupported file format",
        format_: str | None = None,
        supported_formats: list[str] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            format_: The unsupported format.
            supported_formats: List of supported formats.
        """
        details: dict[str, Any] = {}
        if format_:
            details["format"] = format_
        if supported_formats:
            details["supported_formats"] = supported_formats
        super().__init__(
            message=message,
            code="UNSUPPORTED_FORMAT",
            status_code=415,
            details=details,
        )


class DuplicateResourceError(BaseDocxException):
    """Exception raised when attempting to create a duplicate resource."""

    def __init__(
        self,
        message: str = "Resource already exists",
        resource_type: str | None = None,
        identifier: str | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            resource_type: Type of the resource.
            identifier: Resource identifier.
        """
        details: dict[str, Any] = {}
        if resource_type:
            details["resource_type"] = resource_type
        if identifier:
            details["identifier"] = identifier
        super().__init__(
            message=message,
            code="DUPLICATE_RESOURCE",
            status_code=409,
            details=details,
        )


class OperationTimeoutError(BaseDocxException):
    """Exception raised when an operation times out."""

    def __init__(
        self,
        message: str = "Operation timed out",
        operation: str | None = None,
        timeout_seconds: int | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            operation: The operation that timed out.
            timeout_seconds: Timeout duration in seconds.
        """
        details: dict[str, Any] = {}
        if operation:
            details["operation"] = operation
        if timeout_seconds:
            details["timeout_seconds"] = timeout_seconds
        super().__init__(
            message=message,
            code="OPERATION_TIMEOUT",
            status_code=504,
            details=details,
        )


class ExternalServiceError(BaseDocxException):
    """Exception raised when an external service fails."""

    def __init__(
        self,
        message: str = "External service error",
        service: str | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            service: Name of the external service.
        """
        details = {"service": service} if service else {}
        super().__init__(
            message=message,
            code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
            details=details,
        )


class DocumentLockError(BaseDocxException):
    """Exception raised when a document is locked by another user."""

    def __init__(
        self,
        message: str = "Document is locked by another user",
        locked_by: str | None = None,
        lock_expires: str | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            locked_by: User who holds the lock.
            lock_expires: Lock expiration timestamp.
        """
        details: dict[str, Any] = {}
        if locked_by:
            details["locked_by"] = locked_by
        if lock_expires:
            details["lock_expires"] = lock_expires
        super().__init__(
            message=message,
            code="DOCUMENT_LOCKED",
            status_code=423,
            details=details,
        )


class VersionConflictError(BaseDocxException):
    """Exception raised when there's a version conflict."""

    def __init__(
        self,
        message: str = "Version conflict detected",
        current_version: int | None = None,
        expected_version: int | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            current_version: Current version of the resource.
            expected_version: Expected version for the operation.
        """
        details: dict[str, Any] = {}
        if current_version is not None:
            details["current_version"] = current_version
        if expected_version is not None:
            details["expected_version"] = expected_version
        super().__init__(
            message=message,
            code="VERSION_CONFLICT",
            status_code=409,
            details=details,
        )
