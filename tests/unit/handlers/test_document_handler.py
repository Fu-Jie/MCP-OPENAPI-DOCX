"""Unit tests for document handler."""

import pytest
from io import BytesIO
from docx import Document

from src.handlers.document_handler import DocumentHandler


class TestDocumentHandler:
    """Test cases for DocumentHandler class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.handler = DocumentHandler()

    def test_create_document(self):
        """Test creating a new document."""
        doc = self.handler.create_document()
        assert doc is not None
        assert isinstance(doc, Document)

    def test_load_document(self, sample_document_path):
        """Test loading a document from file."""
        doc = self.handler.load_document(sample_document_path)
        assert doc is not None
        assert isinstance(doc, Document)

    def test_load_document_invalid_path(self):
        """Test loading a document from invalid path."""
        with pytest.raises(Exception):
            self.handler.load_document("nonexistent.docx")

    def test_save_document(self, sample_document_path, test_settings):
        """Test saving a document."""
        doc = self.handler.load_document(sample_document_path)
        save_path = f"{test_settings.temp_dir}/saved_test.docx"
        self.handler.save_document(doc, save_path)

        # Verify file was created
        import os
        assert os.path.exists(save_path)

    def test_get_metadata(self, sample_document_path):
        """Test getting document metadata."""
        doc = self.handler.load_document(sample_document_path)
        metadata = self.handler.get_metadata(doc)

        assert isinstance(metadata, dict)
        assert "author" in metadata or metadata == {}

    def test_set_metadata(self, sample_document_path):
        """Test setting document metadata."""
        doc = self.handler.load_document(sample_document_path)
        self.handler.set_metadata(doc, author="Test Author", title="Test Title")

        metadata = self.handler.get_metadata(doc)
        assert metadata.get("author") == "Test Author"

    def test_document_from_bytes(self, sample_docx_content):
        """Test loading document from bytes."""
        doc = self.handler.load_from_bytes(sample_docx_content)
        assert doc is not None
        assert isinstance(doc, Document)

    def test_document_to_bytes(self, sample_document_path):
        """Test converting document to bytes."""
        doc = self.handler.load_document(sample_document_path)
        content = self.handler.to_bytes(doc)

        assert isinstance(content, bytes)
        assert len(content) > 0
        # Verify it's a valid DOCX (starts with PK for ZIP)
        assert content[:2] == b"PK"
