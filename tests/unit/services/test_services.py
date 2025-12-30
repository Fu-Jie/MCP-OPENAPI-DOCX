"""Unit tests for services."""

import pytest
from unittest.mock import MagicMock, AsyncMock


class TestDocumentService:
    """Test cases for DocumentService."""

    def test_service_instantiation(self):
        """Test document service can be instantiated."""
        from src.services.document_service import DocumentService

        # Use a mock db session
        mock_db = MagicMock()
        service = DocumentService(mock_db)

        assert service is not None
        assert service.db == mock_db
        assert service.document_handler is not None


class TestTextService:
    """Test cases for TextService."""

    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.text_service import TextService

        mock_db = MagicMock()
        service = TextService(mock_db)
        assert service is not None
        assert service.document_handler is not None
        assert service.text_handler is not None


class TestTableService:
    """Test cases for TableService."""

    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.table_service import TableService

        mock_db = MagicMock()
        service = TableService(mock_db)
        assert service is not None


class TestExportService:
    """Test cases for ExportService."""

    @pytest.mark.asyncio
    async def test_get_export_formats(self):
        """Test getting available export formats."""
        from src.services.export_service import ExportService

        mock_db = MagicMock()
        service = ExportService(mock_db)
        formats = await service.get_export_formats()

        assert isinstance(formats, list)
        assert len(formats) > 0
        assert any(f["format"] == "pdf" for f in formats)
        assert any(f["format"] == "html" for f in formats)


class TestVersionService:
    """Test cases for VersionService."""

    @pytest.mark.asyncio
    async def test_get_versions_empty(self):
        """Test getting versions for non-existent document."""
        from src.services.version_service import VersionService

        mock_db = MagicMock()
        mock_db.execute = AsyncMock(return_value=MagicMock(scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[])))))
        service = VersionService(mock_db)
        versions = await service.get_versions("non-existent-id")

        assert isinstance(versions, list)
        assert len(versions) == 0
