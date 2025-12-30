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
try:
    import bcrypt as _bcrypt
    
    # Only patch if not already patched
    if not hasattr(_bcrypt.hashpw, '_patched'):
        _original_hashpw = _bcrypt.hashpw
        _original_checkpw = _bcrypt.checkpw
        
        def _truncate_password(password):
            """Truncate password to 72 bytes for bcrypt, preserving UTF-8 boundaries."""
            if isinstance(password, str):
                password = password.encode('utf-8')
            if len(password) > 72:
                # Truncate at 72 bytes, handling UTF-8 multi-byte characters properly
                truncated = password[:72]
                # UTF-8 continuation bytes start with bits 10xxxxxx (0x80-0xBF)
                # Walk backward to remove any trailing continuation bytes
                while truncated and (truncated[-1] & 0xC0) == 0x80:
                    truncated = truncated[:-1]
                # If the last byte is a multi-byte character start, remove it too
                # since we don't have all its continuation bytes
                if truncated and (truncated[-1] & 0x80) != 0:
                    truncated = truncated[:-1]
                password = truncated
            return password
        
        def _patched_hashpw(password, salt):
            """Patched hashpw that truncates passwords to 72 bytes."""
            return _original_hashpw(_truncate_password(password), salt)
        
        def _patched_checkpw(password, hashed_password):
            """Patched checkpw that truncates passwords to 72 bytes."""
            return _original_checkpw(_truncate_password(password), hashed_password)
        
        # Mark as patched to prevent double-patching
        _patched_hashpw._patched = True
        _patched_checkpw._patched = True
        
        _bcrypt.hashpw = _patched_hashpw
        _bcrypt.checkpw = _patched_checkpw
except ImportError:
    pass  # bcrypt not installed

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityUtils:
    """Utility class for security operations.

    Provides static methods for security-related tasks.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password.

        Args:
            password: Plain text password.

        Returns:
            Hashed password.
        
        Note:
            Bcrypt has a 72-byte limit. Passwords are automatically
            truncated to this length, preserving UTF-8 character boundaries.
        """
        # Bcrypt limitation: passwords cannot exceed 72 bytes
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate at 72 bytes, handling UTF-8 multi-byte characters properly
            truncated = password_bytes[:72]
            # UTF-8 continuation bytes start with bits 10xxxxxx (0x80-0xBF)
            # Walk backward to remove any trailing continuation bytes
            while truncated and (truncated[-1] & 0xC0) == 0x80:
                truncated = truncated[:-1]
            # If the last byte is a multi-byte character start, remove it too
            # since we don't have all its continuation bytes
            if truncated and (truncated[-1] & 0x80) != 0:
                truncated = truncated[:-1]
            password = truncated.decode('utf-8')
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
        password_bytes = plain.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate at 72 bytes, handling UTF-8 multi-byte characters properly
            truncated = password_bytes[:72]
            # UTF-8 continuation bytes start with bits 10xxxxxx (0x80-0xBF)
            # Walk backward to remove any trailing continuation bytes
            while truncated and (truncated[-1] & 0xC0) == 0x80:
                truncated = truncated[:-1]
            # If the last byte is a multi-byte character start, remove it too
            # since we don't have all its continuation bytes
            if truncated and (truncated[-1] & 0x80) != 0:
                truncated = truncated[:-1]
            plain = truncated.decode('utf-8')
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
