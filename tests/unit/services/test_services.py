"""Unit tests for services."""

import pytest
from unittest.mock import MagicMock, patch


class TestDocumentService:
    """Test cases for DocumentService."""

    @pytest.mark.asyncio
    async def test_create_document(self, db_session, test_settings):
        """Test document creation."""
        from src.services.document_service import DocumentService

        service = DocumentService(db_session)

        # This test verifies the service can be instantiated
        assert service is not None
        assert service.db == db_session
        assert service.document_handler is not None

    @pytest.mark.asyncio
    async def test_list_documents(self, db_session):
        """Test listing documents."""
        from src.services.document_service import DocumentService

        service = DocumentService(db_session)
        docs, total = await service.list_documents(skip=0, limit=10)

        assert isinstance(docs, list)
        assert isinstance(total, int)


class TestTextService:
    """Test cases for TextService."""

    def test_service_initialization(self, db_session):
        """Test service initialization."""
        from src.services.text_service import TextService

        service = TextService(db_session)
        assert service is not None
        assert service.document_handler is not None
        assert service.text_handler is not None


class TestTableService:
    """Test cases for TableService."""

    def test_service_initialization(self, db_session):
        """Test service initialization."""
        from src.services.table_service import TableService

        service = TableService(db_session)
        assert service is not None


class TestExportService:
    """Test cases for ExportService."""

    @pytest.mark.asyncio
    async def test_get_export_formats(self, db_session):
        """Test getting available export formats."""
        from src.services.export_service import ExportService

        service = ExportService(db_session)
        formats = await service.get_export_formats()

        assert isinstance(formats, list)
        assert len(formats) > 0
        assert any(f["format"] == "pdf" for f in formats)
        assert any(f["format"] == "html" for f in formats)


class TestVersionService:
    """Test cases for VersionService."""

    @pytest.mark.asyncio
    async def test_get_versions_empty(self, db_session):
        """Test getting versions for non-existent document."""
        from src.services.version_service import VersionService

        service = VersionService(db_session)
        versions = await service.get_versions("non-existent-id")

        assert isinstance(versions, list)
        assert len(versions) == 0
