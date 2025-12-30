"""Unit tests for utility modules."""

import pytest
from src.utils.file_utils import FileUtils
from src.utils.validation_utils import ValidationUtils
from src.utils.conversion_utils import ConversionUtils
from src.utils.security_utils import SecurityUtils


class TestFileUtils:
    """Test cases for FileUtils class."""

    def test_get_file_extension(self):
        """Test getting file extension."""
        assert FileUtils.get_file_extension("test.docx") == ".docx"
        assert FileUtils.get_file_extension("path/to/file.pdf") == ".pdf"
        assert FileUtils.get_file_extension("no_extension") == ""

    def test_safe_filename(self):
        """Test filename sanitization."""
        assert FileUtils.safe_filename("test.docx") == "test.docx"
        assert FileUtils.safe_filename("test<>file.docx") == "testfile.docx"
        assert FileUtils.safe_filename("  test  ") == "test"
        assert FileUtils.safe_filename("") == "unnamed"


class TestValidationUtils:
    """Test cases for ValidationUtils class."""

    def test_is_valid_document_extension(self):
        """Test document extension validation."""
        assert ValidationUtils.is_valid_document_extension("test.docx") is True
        assert ValidationUtils.is_valid_document_extension("test.doc") is True
        assert ValidationUtils.is_valid_document_extension("test.pdf") is False

    def test_is_valid_image_extension(self):
        """Test image extension validation."""
        assert ValidationUtils.is_valid_image_extension("test.png") is True
        assert ValidationUtils.is_valid_image_extension("test.jpg") is True
        assert ValidationUtils.is_valid_image_extension("test.docx") is False

    def test_is_valid_email(self):
        """Test email validation."""
        assert ValidationUtils.is_valid_email("test@example.com") is True
        assert ValidationUtils.is_valid_email("invalid-email") is False

    def test_is_valid_uuid(self):
        """Test UUID validation."""
        assert ValidationUtils.is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") is True
        assert ValidationUtils.is_valid_uuid("invalid-uuid") is False

    def test_is_valid_color(self):
        """Test color validation."""
        assert ValidationUtils.is_valid_color("#FF0000") is True
        assert ValidationUtils.is_valid_color("FF0000") is True
        assert ValidationUtils.is_valid_color("#F00") is True
        assert ValidationUtils.is_valid_color("invalid") is False

    def test_validate_pagination(self):
        """Test pagination validation."""
        skip, limit = ValidationUtils.validate_pagination(0, 10)
        assert skip == 0
        assert limit == 10

        skip, limit = ValidationUtils.validate_pagination(-5, 200, max_limit=50)
        assert skip == 0
        assert limit == 50

    def test_is_docx_file(self):
        """Test DOCX file validation."""
        assert ValidationUtils.is_docx_file(b"PK...") is True
        assert ValidationUtils.is_docx_file(b"Hello") is False


class TestConversionUtils:
    """Test cases for ConversionUtils class."""

    def test_inches_to_cm(self):
        """Test inches to cm conversion."""
        result = ConversionUtils.inches_to_cm(1)
        assert abs(result - 2.54) < 0.01

    def test_cm_to_inches(self):
        """Test cm to inches conversion."""
        result = ConversionUtils.cm_to_inches(2.54)
        assert abs(result - 1) < 0.01

    def test_hex_to_rgb(self):
        """Test hex to RGB conversion."""
        r, g, b = ConversionUtils.hex_to_rgb("#FF0000")
        assert (r, g, b) == (255, 0, 0)

        r, g, b = ConversionUtils.hex_to_rgb("00FF00")
        assert (r, g, b) == (0, 255, 0)

    def test_rgb_to_hex(self):
        """Test RGB to hex conversion."""
        assert ConversionUtils.rgb_to_hex(255, 0, 0) == "#ff0000"
        assert ConversionUtils.rgb_to_hex(0, 255, 0) == "#00ff00"

    def test_bytes_to_human_readable(self):
        """Test bytes to human readable conversion."""
        assert "1.00 KB" in ConversionUtils.bytes_to_human_readable(1024)
        assert "1.00 MB" in ConversionUtils.bytes_to_human_readable(1024 * 1024)


class TestSecurityUtils:
    """Test cases for SecurityUtils class."""

    def test_hash_and_verify_password(self):
        """Test password hashing and verification."""
        password = "test_password_123"
        hashed = SecurityUtils.hash_password(password)

        assert hashed != password
        assert SecurityUtils.verify_password(password, hashed) is True
        assert SecurityUtils.verify_password("wrong_password", hashed) is False

    def test_generate_token(self):
        """Test token generation."""
        token = SecurityUtils.generate_token(16)
        assert len(token) == 32  # Hex representation is 2x length
        assert token.isalnum()

    def test_generate_api_key(self):
        """Test API key generation."""
        api_key = SecurityUtils.generate_api_key()
        assert api_key.startswith("docx_")

    def test_sha256_hash(self):
        """Test SHA-256 hashing."""
        hash1 = SecurityUtils.sha256_hash("test")
        hash2 = SecurityUtils.sha256_hash("test")
        hash3 = SecurityUtils.sha256_hash("different")

        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64

    def test_mask_sensitive_data(self):
        """Test data masking."""
        masked = SecurityUtils.mask_sensitive_data("1234567890", visible_chars=4)
        assert masked == "1234******"

    def test_is_strong_password(self):
        """Test password strength validation."""
        is_strong, issues = SecurityUtils.is_strong_password("Weak")
        assert is_strong is False
        assert len(issues) > 0

        is_strong, issues = SecurityUtils.is_strong_password("Strong@Password1")
        assert is_strong is True
        assert len(issues) == 0
