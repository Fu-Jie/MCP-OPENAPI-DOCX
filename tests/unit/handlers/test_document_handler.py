"""Unit tests for document handler."""

import os

import pytest
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

    def test_open_document(self, sample_document_path):
        """Test opening a document from file."""
        doc = self.handler.open_document(sample_document_path)
        assert doc is not None
        assert isinstance(doc, Document)

    def test_open_document_invalid_path(self):
        """Test opening a document from invalid path."""
        with pytest.raises(Exception):
            self.handler.open_document("nonexistent.docx")

    def test_save_document(self, sample_document_path, test_settings):
        """Test saving a document."""
        self.handler.open_document(sample_document_path)
        save_path = f"{test_settings.temp_dir}/saved_test.docx"
        self.handler.save_document(save_path)

        # Verify file was created
        assert os.path.exists(save_path)

    def test_get_metadata(self, sample_document_path):
        """Test getting document metadata."""
        self.handler.open_document(sample_document_path)
        metadata = self.handler.get_metadata()

        # Metadata is a DTO object
        assert metadata is not None

    def test_set_metadata(self, sample_document_path):
        """Test setting document metadata."""
        self.handler.open_document(sample_document_path)
        self.handler.set_metadata(author="Test Author", title="Test Title")

        metadata = self.handler.get_metadata()
        assert metadata.author == "Test Author"

    def test_document_from_bytes(self, sample_docx_content):
        """Test loading document from bytes."""
        doc = self.handler.open_from_bytes(sample_docx_content)
        assert doc is not None
        assert isinstance(doc, Document)

    def test_document_to_bytes(self, sample_document_path):
        """Test converting document to bytes."""
        self.handler.open_document(sample_document_path)
        content = self.handler.save_to_bytes()

        assert isinstance(content, bytes)
        assert len(content) > 0
        # Verify it's a valid DOCX (starts with PK for ZIP)
        assert content[:2] == b"PK"
