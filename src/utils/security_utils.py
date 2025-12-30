"""Security utility functions.

This module provides security utilities for encryption,
password handling, and token generation.
"""

import base64
import hashlib
import hmac
import secrets

# Monkey-patch bcrypt to handle 72-byte limit before passlib loads
# This ensures compatibility with bcrypt>=4.0.0 which enforces the limit strictly


def _truncate_to_72_bytes_utf8_safe(data):
    """Truncate data to 72 bytes, preserving UTF-8 character boundaries.

    Args:
        data: String or bytes to truncate.

    Returns:
        bytes: Truncated data that is valid UTF-8 and <= 72 bytes.

    Note:
        This helper is used by both the bcrypt monkey-patch and SecurityUtils.
        It handles UTF-8 multi-byte characters properly to avoid partial characters.

        UTF-8 Encoding:
        - 0x00-0x7F: Single-byte characters (ASCII)
        - 0x80-0xBF: Continuation bytes (10xxxxxx)
        - 0xC0-0xDF: 2-byte sequence start (110xxxxx)
        - 0xE0-0xEF: 3-byte sequence start (1110xxxx)
        - 0xF0-0xF7: 4-byte sequence start (11110xxx)
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    if len(data) <= 72:
        return data

    # Truncate at 72 bytes
    truncated = data[:72]

    # UTF-8 continuation bytes start with bits 10xxxxxx (0x80-0xBF)
    # Walk backward to remove any trailing continuation bytes
    while truncated and (truncated[-1] & 0xC0) == 0x80:
        truncated = truncated[:-1]

    # If the last byte is a multi-byte character start (>= 0xC0), remove it too
    # since we don't have all its continuation bytes.
    # Note: In UTF-8, bytes >= 0xC0 are ALWAYS multi-byte sequence starts.
    # There are no valid single-byte characters with values >= 0x80 in UTF-8.
    if truncated and truncated[-1] >= 0xC0:
        truncated = truncated[:-1]

    return truncated


# Monkey-patch bcrypt to handle 72-byte limit before passlib loads
# This ensures compatibility with bcrypt>=4.0.0 which enforces the limit strictly

# Track whether bcrypt has been patched (module import is thread-safe in Python)
_bcrypt_patched = False

try:
    import bcrypt as _bcrypt

    if not _bcrypt_patched:
        _original_hashpw = _bcrypt.hashpw
        _original_checkpw = _bcrypt.checkpw

        def _patched_hashpw(password, salt):
            """Patched hashpw that truncates passwords to 72 bytes."""
            return _original_hashpw(_truncate_to_72_bytes_utf8_safe(password), salt)

        def _patched_checkpw(password, hashed_password):
            """Patched checkpw that truncates passwords to 72 bytes."""
            return _original_checkpw(
                _truncate_to_72_bytes_utf8_safe(password), hashed_password
            )

        _bcrypt.hashpw = _patched_hashpw
        _bcrypt.checkpw = _patched_checkpw
        _bcrypt_patched = True
except ImportError:
    pass  # bcrypt not installed

from passlib.context import CryptContext  # noqa: E402

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityUtils:
    """Utility class for security operations.

    Provides static methods for security-related tasks.
    """

    @staticmethod
    def _truncate_password_to_72_bytes(password: str) -> str:
        """Truncate password to 72 bytes, preserving UTF-8 character boundaries.

        Args:
            password: Password string to truncate.

        Returns:
            Truncated password string that is valid UTF-8 and <= 72 bytes.

        Note:
            This is an internal helper method that handles bcrypt's 72-byte limit.
            It uses the shared _truncate_to_72_bytes_utf8_safe() function.
            The algorithm ensures valid UTF-8 output by properly handling
            multi-byte character boundaries.
        """
        truncated_bytes = _truncate_to_72_bytes_utf8_safe(password)
        # The truncation algorithm guarantees valid UTF-8, but be defensive
        try:
            return truncated_bytes.decode("utf-8")
        except UnicodeDecodeError:
            # This should never happen with the current algorithm, but if it does,
            # fall back to strict truncation with error handling
            return truncated_bytes.decode("utf-8", errors="ignore")

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password.

        Returns:
            Hashed password.

        Note:
            Bcrypt has a 72-byte limit. Passwords longer than 72 bytes are
            automatically truncated to this length, preserving UTF-8 character
            boundaries. This means that:

            - Passwords of 72 bytes or less are hashed in full
            - Passwords longer than 72 bytes are truncated before hashing
            - The same truncation is applied during verification
            - Two passwords that differ only after byte 72 will hash identically

            Security Implications:
            If your application requires passwords longer than 72 bytes, consider
            pre-hashing the password (e.g., with SHA-256) before passing it to
            this method to ensure the full password is used.
        """
        # Bcrypt limitation: passwords cannot exceed 72 bytes
        password = SecurityUtils._truncate_password_to_72_bytes(password)
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Verify a password against hash.

        Args:
            plain: Plain text password.
            hashed: Hashed password.

        Returns:
            True if password matches.
        """
        # Apply same truncation as in hash_password for consistency
        plain = SecurityUtils._truncate_password_to_72_bytes(plain)
        return pwd_context.verify(plain, hashed)

    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a secure random token.

        Args:
            length: Token length in bytes.

        Returns:
            Hex token string.
        """
        return secrets.token_hex(length)

    @staticmethod
    def generate_url_safe_token(length: int = 32) -> str:
        """Generate a URL-safe token.

        Args:
            length: Token length in bytes.

        Returns:
            URL-safe token string.
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_api_key() -> str:
        """Generate an API key.

        Returns:
            API key string.
        """
        return f"docx_{secrets.token_hex(24)}"

    @staticmethod
    def sha256_hash(data: str | bytes) -> str:
        """Calculate SHA-256 hash.

        Args:
            data: Data to hash.

        Returns:
            Hash string.
        """
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def sha512_hash(data: str | bytes) -> str:
        """Calculate SHA-512 hash.

        Args:
            data: Data to hash.

        Returns:
            Hash string.
        """
        if isinstance(data, str):
            data = data.encode()
        return hashlib.sha512(data).hexdigest()

    @staticmethod
    def hmac_sign(
        data: str | bytes,
        key: str | bytes,
        algorithm: str = "sha256",
    ) -> str:
        """Create HMAC signature.

        Args:
            data: Data to sign.
            key: Secret key.
            algorithm: Hash algorithm.

        Returns:
            HMAC signature.
        """
        if isinstance(data, str):
            data = data.encode()
        if isinstance(key, str):
            key = key.encode()
        return hmac.new(key, data, algorithm).hexdigest()

    @staticmethod
    def verify_hmac(
        data: str | bytes,
        signature: str,
        key: str | bytes,
        algorithm: str = "sha256",
    ) -> bool:
        """Verify HMAC signature.

        Args:
            data: Original data.
            signature: HMAC signature.
            key: Secret key.
            algorithm: Hash algorithm.

        Returns:
            True if signature is valid.
        """
        expected = SecurityUtils.hmac_sign(data, key, algorithm)
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def base64_encode(data: bytes) -> str:
        """Encode bytes to base64.

        Args:
            data: Data to encode.

        Returns:
            Base64 string.
        """
        return base64.b64encode(data).decode()

    @staticmethod
    def base64_decode(data: str) -> bytes:
        """Decode base64 to bytes.

        Args:
            data: Base64 string.

        Returns:
            Decoded bytes.
        """
        return base64.b64decode(data)

    @staticmethod
    def constant_time_compare(a: str, b: str) -> bool:
        """Compare strings in constant time.

        Args:
            a: First string.
            b: Second string.

        Returns:
            True if strings are equal.
        """
        return hmac.compare_digest(a, b)

    @staticmethod
    def mask_sensitive_data(
        data: str,
        visible_chars: int = 4,
        mask_char: str = "*",
    ) -> str:
        """Mask sensitive data.

        Args:
            data: Data to mask.
            visible_chars: Number of visible characters.
            mask_char: Character to use for masking.

        Returns:
            Masked string.
        """
        if len(data) <= visible_chars:
            return mask_char * len(data)
        return data[:visible_chars] + mask_char * (len(data) - visible_chars)

    @staticmethod
    def sanitize_input(data: str) -> str:
        """Sanitize user input.

        Args:
            data: User input.

        Returns:
            Sanitized string.
        """
        # Remove potential script injections
        dangerous = ["<script", "</script", "javascript:", "onerror", "onload"]
        result = data
        for pattern in dangerous:
            result = result.replace(pattern, "")
            result = result.replace(pattern.upper(), "")
        return result

    @staticmethod
    def is_strong_password(password: str) -> tuple[bool, list[str]]:
        """Check password strength.

        Args:
            password: Password to check.

        Returns:
            Tuple of (is_strong, list of issues).
        """
        issues = []

        if len(password) < 8:
            issues.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            issues.append("Password must contain uppercase letter")
        if not any(c.islower() for c in password):
            issues.append("Password must contain lowercase letter")
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain a number")
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            issues.append("Password must contain a special character")

        return len(issues) == 0, issues
