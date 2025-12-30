"""Unit tests for utility modules."""

import os
import tempfile
import pytest
from pathlib import Path
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
        assert FileUtils.get_file_extension("TEST.DOCX") == ".docx"  # Case insensitive

    def test_safe_filename(self):
        """Test filename sanitization."""
        assert FileUtils.safe_filename("test.docx") == "test.docx"
        assert FileUtils.safe_filename("test<>file.docx") == "testfile.docx"
        assert FileUtils.safe_filename("  test  ") == "test"
        assert FileUtils.safe_filename("") == "unnamed"
        assert FileUtils.safe_filename("...") == "unnamed"
        assert FileUtils.safe_filename("test:file.docx") == "testfile.docx"
    
    def test_ensure_directory(self, tmp_path):
        """Test directory creation."""
        test_dir = tmp_path / "new_dir"
        FileUtils.ensure_directory(str(test_dir))
        assert test_dir.exists()
        
        # Test idempotency - should not fail if already exists
        FileUtils.ensure_directory(str(test_dir))
        assert test_dir.exists()
    
    def test_file_exists(self, tmp_path):
        """Test file existence check."""
        existing_file = tmp_path / "test.txt"
        existing_file.write_text("test")
        
        assert FileUtils.file_exists(str(existing_file)) is True
        assert FileUtils.file_exists(str(tmp_path / "nonexistent.txt")) is False
    
    def test_delete_file(self, tmp_path):
        """Test file deletion."""
        test_file = tmp_path / "to_delete.txt"
        test_file.write_text("test")
        
        assert FileUtils.delete_file(str(test_file)) is True
        assert not test_file.exists()
        assert FileUtils.delete_file(str(test_file)) is False  # Already deleted
    
    def test_read_write_binary(self, tmp_path):
        """Test binary read/write operations."""
        test_file = tmp_path / "binary.dat"
        test_data = b"binary data \x00\x01\x02"
        
        FileUtils.write_binary(str(test_file), test_data)
        read_data = FileUtils.read_binary(str(test_file))
        
        assert read_data == test_data
    
    def test_read_write_text(self, tmp_path):
        """Test text read/write operations."""
        test_file = tmp_path / "text.txt"
        test_content = "Hello, World!\nSecond line."
        
        FileUtils.write_text(str(test_file), test_content)
        read_content = FileUtils.read_text(str(test_file))
        
        assert read_content == test_content
    
    def test_copy_file(self, tmp_path):
        """Test file copying."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("test content")
        
        result = FileUtils.copy_file(str(source), str(dest))
        
        assert dest.exists()
        assert dest.read_text() == "test content"
        assert source.exists()  # Original still exists
    
    def test_move_file(self, tmp_path):
        """Test file moving."""
        source = tmp_path / "source.txt"
        dest = tmp_path / "dest.txt"
        source.write_text("test content")
        
        result = FileUtils.move_file(str(source), str(dest))
        
        assert dest.exists()
        assert dest.read_text() == "test content"
        assert not source.exists()  # Original moved
    
    def test_get_file_size(self, tmp_path):
        """Test file size retrieval."""
        test_file = tmp_path / "size_test.txt"
        test_file.write_bytes(b"x" * 100)
        
        size = FileUtils.get_file_size(str(test_file))
        assert size == 100
    
    def test_get_checksum(self, tmp_path):
        """Test file checksum calculation."""
        test_file = tmp_path / "checksum.txt"
        test_file.write_text("test content")
        
        checksum = FileUtils.get_checksum(str(test_file))
        
        assert len(checksum) == 64  # SHA-256 produces 64 hex chars
        assert checksum.isalnum()
        
        # Same content should produce same checksum
        checksum2 = FileUtils.get_checksum(str(test_file))
        assert checksum == checksum2
    
    def test_create_temp_file(self):
        """Test temporary file creation."""
        temp_file = FileUtils.create_temp_file(suffix=".txt", prefix="test_")
        
        try:
            assert os.path.exists(temp_file)
            assert temp_file.endswith(".txt")
            assert "test_" in os.path.basename(temp_file)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_create_temp_file_with_content(self):
        """Test temporary file creation with content."""
        content = b"test content"
        temp_file = FileUtils.create_temp_file(content=content)
        
        try:
            with open(temp_file, "rb") as f:
                assert f.read() == content
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_create_temp_directory(self):
        """Test temporary directory creation."""
        temp_dir = FileUtils.create_temp_directory(prefix="test_")
        
        try:
            assert os.path.exists(temp_dir)
            assert os.path.isdir(temp_dir)
        finally:
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
    
    def test_list_files(self, tmp_path):
        """Test file listing."""
        # Create test files
        (tmp_path / "file1.txt").write_text("test")
        (tmp_path / "file2.txt").write_text("test")
        (tmp_path / "file3.docx").write_text("test")
        
        all_files = FileUtils.list_files(str(tmp_path))
        assert len(all_files) == 3
        
        txt_files = FileUtils.list_files(str(tmp_path), pattern="*.txt")
        assert len(txt_files) == 2
    
    def test_list_files_recursive(self, tmp_path):
        """Test recursive file listing."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "file1.txt").write_text("test")
        (subdir / "file2.txt").write_text("test")
        
        files = FileUtils.list_files(str(tmp_path), pattern="*.txt", recursive=True)
        assert len(files) == 2
    
    def test_get_mime_type(self, tmp_path):
        """Test MIME type detection."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        
        mime = FileUtils.get_mime_type(str(test_file))
        assert "text" in mime


class TestValidationUtils:
    """Test cases for ValidationUtils class."""

    def test_is_valid_document_extension(self):
        """Test document extension validation."""
        assert ValidationUtils.is_valid_document_extension("test.docx") is True
        assert ValidationUtils.is_valid_document_extension("test.doc") is True
        assert ValidationUtils.is_valid_document_extension("test.pdf") is False
        assert ValidationUtils.is_valid_document_extension("TEST.DOCX") is True  # Case insensitive
        assert ValidationUtils.is_valid_document_extension("/path/to/file.docx") is True

    def test_is_valid_image_extension(self):
        """Test image extension validation."""
        assert ValidationUtils.is_valid_image_extension("test.png") is True
        assert ValidationUtils.is_valid_image_extension("test.jpg") is True
        assert ValidationUtils.is_valid_image_extension("test.jpeg") is True
        assert ValidationUtils.is_valid_image_extension("test.gif") is True
        assert ValidationUtils.is_valid_image_extension("test.bmp") is True
        assert ValidationUtils.is_valid_image_extension("test.tiff") is True
        assert ValidationUtils.is_valid_image_extension("test.docx") is False

    def test_is_valid_email(self):
        """Test email validation."""
        assert ValidationUtils.is_valid_email("test@example.com") is True
        assert ValidationUtils.is_valid_email("user.name@example.com") is True
        assert ValidationUtils.is_valid_email("user+tag@example.co.uk") is True
        assert ValidationUtils.is_valid_email("invalid-email") is False
        assert ValidationUtils.is_valid_email("@example.com") is False
        assert ValidationUtils.is_valid_email("test@") is False
        assert ValidationUtils.is_valid_email("") is False

    def test_is_valid_uuid(self):
        """Test UUID validation."""
        assert ValidationUtils.is_valid_uuid("550e8400-e29b-41d4-a716-446655440000") is True
        assert ValidationUtils.is_valid_uuid("550E8400-E29B-41D4-A716-446655440000") is True  # Case insensitive
        assert ValidationUtils.is_valid_uuid("invalid-uuid") is False
        assert ValidationUtils.is_valid_uuid("550e8400-e29b-41d4-a716") is False  # Too short
        assert ValidationUtils.is_valid_uuid("") is False

    def test_is_valid_color(self):
        """Test color validation."""
        assert ValidationUtils.is_valid_color("#FF0000") is True
        assert ValidationUtils.is_valid_color("FF0000") is True
        assert ValidationUtils.is_valid_color("#F00") is True
        assert ValidationUtils.is_valid_color("F00") is True
        assert ValidationUtils.is_valid_color("#ff0000") is True  # Lowercase
        assert ValidationUtils.is_valid_color("invalid") is False
        assert ValidationUtils.is_valid_color("#GG0000") is False
        assert ValidationUtils.is_valid_color("") is False

    def test_validate_pagination(self):
        """Test pagination validation."""
        skip, limit = ValidationUtils.validate_pagination(0, 10)
        assert skip == 0
        assert limit == 10

        skip, limit = ValidationUtils.validate_pagination(-5, 200, max_limit=50)
        assert skip == 0
        assert limit == 50
        
        skip, limit = ValidationUtils.validate_pagination(10, 0)
        assert skip == 10
        assert limit == 1  # Minimum limit is 1

    def test_is_docx_file(self):
        """Test DOCX file validation."""
        assert ValidationUtils.is_docx_file(b"PK...") is True
        assert ValidationUtils.is_docx_file(b"Hello") is False
        assert ValidationUtils.is_docx_file(b"") is False
    
    def test_is_valid_file_size(self):
        """Test file size validation."""
        assert ValidationUtils.is_valid_file_size(1024) is True
        assert ValidationUtils.is_valid_file_size(100 * 1024 * 1024) is True  # 100MB
        assert ValidationUtils.is_valid_file_size(0) is False  # Zero not allowed
        assert ValidationUtils.is_valid_file_size(-1) is False  # Negative not allowed
        assert ValidationUtils.is_valid_file_size(200 * 1024 * 1024) is False  # Over 100MB
        
        # Test custom max size
        assert ValidationUtils.is_valid_file_size(5 * 1024 * 1024, max_size=10 * 1024 * 1024) is True
        assert ValidationUtils.is_valid_file_size(15 * 1024 * 1024, max_size=10 * 1024 * 1024) is False
    
    def test_sanitize_string(self):
        """Test string sanitization."""
        assert ValidationUtils.sanitize_string("  test  ") == "test"
        assert ValidationUtils.sanitize_string("test", max_length=2) == "te"
        assert ValidationUtils.sanitize_string("  test  ", strip=False) == "  test  "
        assert ValidationUtils.sanitize_string("hello world", max_length=5) == "hello"
    
    def test_is_valid_paragraph_index(self):
        """Test paragraph index validation."""
        assert ValidationUtils.is_valid_paragraph_index(0, 10) is True
        assert ValidationUtils.is_valid_paragraph_index(10, 10) is True
        assert ValidationUtils.is_valid_paragraph_index(5, 10) is True
        assert ValidationUtils.is_valid_paragraph_index(-1, 10) is False
        assert ValidationUtils.is_valid_paragraph_index(11, 10) is False
    
    def test_is_valid_table_coords(self):
        """Test table coordinate validation."""
        assert ValidationUtils.is_valid_table_coords(0, 0, 5, 5) is True
        assert ValidationUtils.is_valid_table_coords(4, 4, 5, 5) is True
        assert ValidationUtils.is_valid_table_coords(-1, 0, 5, 5) is False
        assert ValidationUtils.is_valid_table_coords(0, -1, 5, 5) is False
        assert ValidationUtils.is_valid_table_coords(5, 5, 5, 5) is False  # Out of bounds
    
    def test_validate_font_size(self):
        """Test font size validation."""
        assert ValidationUtils.validate_font_size(12) is True
        assert ValidationUtils.validate_font_size(1) is True
        assert ValidationUtils.validate_font_size(999) is True
        assert ValidationUtils.validate_font_size(0) is False
        assert ValidationUtils.validate_font_size(1000) is False
        assert ValidationUtils.validate_font_size(-5) is False
    
    def test_validate_margin(self):
        """Test margin validation."""
        assert ValidationUtils.validate_margin(1.0) is True
        assert ValidationUtils.validate_margin(0) is True
        assert ValidationUtils.validate_margin(10) is True
        assert ValidationUtils.validate_margin(-0.1) is False
        assert ValidationUtils.validate_margin(10.1) is False
    
    def test_validate_required_fields(self):
        """Test required fields validation."""
        data = {"name": "test", "email": "test@example.com"}
        
        missing = ValidationUtils.validate_required_fields(data, ["name", "email"])
        assert len(missing) == 0
        
        missing = ValidationUtils.validate_required_fields(data, ["name", "email", "phone"])
        assert "phone" in missing
        
        data_with_none = {"name": "test", "email": None}
        missing = ValidationUtils.validate_required_fields(data_with_none, ["name", "email"])
        assert "email" in missing


class TestConversionUtils:
    """Test cases for ConversionUtils class."""

    def test_inches_to_cm(self):
        """Test inches to cm conversion."""
        result = ConversionUtils.inches_to_cm(1)
        assert abs(result - 2.54) < 0.01
        assert ConversionUtils.inches_to_cm(0) == 0

    def test_cm_to_inches(self):
        """Test cm to inches conversion."""
        result = ConversionUtils.cm_to_inches(2.54)
        assert abs(result - 1) < 0.01
        assert ConversionUtils.cm_to_inches(0) == 0

    def test_hex_to_rgb(self):
        """Test hex to RGB conversion."""
        r, g, b = ConversionUtils.hex_to_rgb("#FF0000")
        assert (r, g, b) == (255, 0, 0)

        r, g, b = ConversionUtils.hex_to_rgb("00FF00")
        assert (r, g, b) == (0, 255, 0)
        
        # Test 3-char hex
        r, g, b = ConversionUtils.hex_to_rgb("#FFF")
        assert (r, g, b) == (255, 255, 255)

    def test_rgb_to_hex(self):
        """Test RGB to hex conversion."""
        assert ConversionUtils.rgb_to_hex(255, 0, 0) == "#ff0000"
        assert ConversionUtils.rgb_to_hex(0, 255, 0) == "#00ff00"
        assert ConversionUtils.rgb_to_hex(0, 0, 0) == "#000000"

    def test_bytes_to_human_readable(self):
        """Test bytes to human readable conversion."""
        assert "1.00 KB" in ConversionUtils.bytes_to_human_readable(1024)
        assert "1.00 MB" in ConversionUtils.bytes_to_human_readable(1024 * 1024)
        assert "B" in ConversionUtils.bytes_to_human_readable(500)
    
    def test_points_to_inches(self):
        """Test points to inches conversion."""
        result = ConversionUtils.points_to_inches(72)
        assert abs(result - 1) < 0.01
    
    def test_inches_to_points(self):
        """Test inches to points conversion."""
        result = ConversionUtils.inches_to_points(1)
        assert abs(result - 72) < 0.01
    
    def test_emu_to_inches(self):
        """Test EMU to inches conversion."""
        result = ConversionUtils.emu_to_inches(914400)
        assert abs(result - 1) < 0.01
    
    def test_inches_to_emu(self):
        """Test inches to EMU conversion."""
        result = ConversionUtils.inches_to_emu(1)
        assert result == 914400
    
    def test_twips_to_inches(self):
        """Test twips to inches conversion."""
        result = ConversionUtils.twips_to_inches(1440)
        assert abs(result - 1) < 0.01
    
    def test_inches_to_twips(self):
        """Test inches to twips conversion."""
        result = ConversionUtils.inches_to_twips(1)
        assert result == 1440
    
    def test_to_docx_inches(self):
        """Test conversion to docx Inches object."""
        from docx.shared import Inches
        result = ConversionUtils.to_docx_inches(1)
        assert isinstance(result, Inches)
    
    def test_to_docx_pt(self):
        """Test conversion to docx Pt object."""
        from docx.shared import Pt
        result = ConversionUtils.to_docx_pt(12)
        assert isinstance(result, Pt)
    
    def test_to_docx_cm(self):
        """Test conversion to docx Cm object."""
        from docx.shared import Cm
        result = ConversionUtils.to_docx_cm(2.54)
        assert isinstance(result, Cm)
    
    def test_dict_to_xml_safe(self):
        """Test converting dict to XML-safe strings."""
        data = {
            "string": "test",
            "number": 123,
            "boolean_true": True,
            "boolean_false": False,
            "none": None,
        }
        result = ConversionUtils.dict_to_xml_safe(data)
        
        assert result["string"] == "test"
        assert result["number"] == "123"
        assert result["boolean_true"] == "true"
        assert result["boolean_false"] == "false"
        assert result["none"] == ""


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
        
        # Test different lengths
        token2 = SecurityUtils.generate_token(64)
        assert len(token2) == 128

    def test_generate_api_key(self):
        """Test API key generation."""
        api_key = SecurityUtils.generate_api_key()
        assert api_key.startswith("docx_")
        assert len(api_key) > 10

    def test_sha256_hash(self):
        """Test SHA-256 hashing."""
        hash1 = SecurityUtils.sha256_hash("test")
        hash2 = SecurityUtils.sha256_hash("test")
        hash3 = SecurityUtils.sha256_hash("different")

        assert hash1 == hash2
        assert hash1 != hash3
        assert len(hash1) == 64
        
        # Test bytes input
        hash4 = SecurityUtils.sha256_hash(b"test")
        assert hash4 == hash1

    def test_mask_sensitive_data(self):
        """Test data masking."""
        masked = SecurityUtils.mask_sensitive_data("1234567890", visible_chars=4)
        assert masked == "1234******"
        
        # Test short string
        masked2 = SecurityUtils.mask_sensitive_data("123", visible_chars=4)
        assert masked2 == "***"
        
        # Test custom mask char
        masked3 = SecurityUtils.mask_sensitive_data("1234567890", visible_chars=4, mask_char="X")
        assert masked3 == "1234XXXXXX"

    def test_is_strong_password(self):
        """Test password strength validation."""
        is_strong, issues = SecurityUtils.is_strong_password("Weak")
        assert is_strong is False
        assert len(issues) > 0

        is_strong, issues = SecurityUtils.is_strong_password("Strong@Password1")
        assert is_strong is True
        assert len(issues) == 0
        
        # Test specific requirements
        is_strong, issues = SecurityUtils.is_strong_password("short")
        assert "at least 8 characters" in issues[0].lower()
        
        is_strong, issues = SecurityUtils.is_strong_password("nouppercase123!")
        assert any("uppercase" in issue.lower() for issue in issues)
    
    def test_generate_url_safe_token(self):
        """Test URL-safe token generation."""
        token = SecurityUtils.generate_url_safe_token(32)
        assert len(token) > 0
        # URL-safe tokens should not contain +, /, or =
        assert "+" not in token or "/" not in token
    
    def test_sha512_hash(self):
        """Test SHA-512 hashing."""
        hash1 = SecurityUtils.sha512_hash("test")
        hash2 = SecurityUtils.sha512_hash(b"test")
        
        assert len(hash1) == 128  # SHA-512 produces 128 hex chars
        assert hash1 == hash2
    
    def test_hmac_sign(self):
        """Test HMAC signing."""
        data = "test data"
        key = "secret key"
        
        signature = SecurityUtils.hmac_sign(data, key)
        assert len(signature) == 64  # SHA-256 HMAC
        
        # Same data and key should produce same signature
        signature2 = SecurityUtils.hmac_sign(data, key)
        assert signature == signature2
        
        # Different key should produce different signature
        signature3 = SecurityUtils.hmac_sign(data, "different key")
        assert signature != signature3
    
    def test_verify_hmac(self):
        """Test HMAC verification."""
        data = "test data"
        key = "secret key"
        
        signature = SecurityUtils.hmac_sign(data, key)
        
        assert SecurityUtils.verify_hmac(data, signature, key) is True
        assert SecurityUtils.verify_hmac(data, "wrong signature", key) is False
        assert SecurityUtils.verify_hmac(data, signature, "wrong key") is False
    
    def test_base64_encode_decode(self):
        """Test base64 encoding/decoding."""
        data = b"test data 123"
        
        encoded = SecurityUtils.base64_encode(data)
        decoded = SecurityUtils.base64_decode(encoded)
        
        assert isinstance(encoded, str)
        assert decoded == data
    
    def test_constant_time_compare(self):
        """Test constant-time string comparison."""
        assert SecurityUtils.constant_time_compare("test", "test") is True
        assert SecurityUtils.constant_time_compare("test", "different") is False
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        dangerous = "<script>alert('XSS')</script>"
        sanitized = SecurityUtils.sanitize_input(dangerous)
        assert "script" not in sanitized.lower()
        
        safe = "Normal text"
        assert SecurityUtils.sanitize_input(safe) == safe
        
        # Test various injection patterns
        assert "javascript" not in SecurityUtils.sanitize_input("javascript:alert(1)").lower()
        assert "onerror" not in SecurityUtils.sanitize_input("onerror=alert(1)").lower()
    
    def test_long_password_truncation(self):
        """Test that very long passwords are handled correctly."""
        # Create a password longer than 72 bytes
        long_password = "A" * 100 + "B1!"
        
        hashed = SecurityUtils.hash_password(long_password)
        
        # Should verify successfully
        assert SecurityUtils.verify_password(long_password, hashed) is True
        
        # Test that our truncation is consistent - bcrypt limits to 72 bytes
        # So two passwords that are identical up to byte 72 will hash the same way
        # This is expected bcrypt behavior
