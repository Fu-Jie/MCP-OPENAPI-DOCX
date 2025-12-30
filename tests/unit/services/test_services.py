"""Unit tests for services."""

import pytest
from unittest.mock import MagicMock, AsyncMock, Mock


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
        assert service.settings is not None


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
        assert service.document_handler is not None
        assert service.table_handler is not None


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


class TestCommentService:
    """Test cases for CommentService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.comment_service import CommentService
        
        mock_db = MagicMock()
        service = CommentService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestSearchService:
    """Test cases for SearchService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.search_service import SearchService
        
        mock_db = MagicMock()
        service = SearchService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestLayoutService:
    """Test cases for LayoutService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.layout_service import LayoutService
        
        mock_db = MagicMock()
        service = LayoutService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestStyleService:
    """Test cases for StyleService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.style_service import StyleService
        
        mock_db = MagicMock()
        service = StyleService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestMediaService:
    """Test cases for MediaService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.media_service import MediaService
        
        mock_db = MagicMock()
        service = MediaService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestListService:
    """Test cases for ListService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.list_service import ListService
        
        mock_db = MagicMock()
        service = ListService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestTocService:
    """Test cases for TocService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.toc_service import TocService
        
        mock_db = MagicMock()
        service = TocService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestRevisionService:
    """Test cases for RevisionService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.revision_service import RevisionService
        
        mock_db = MagicMock()
        service = RevisionService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestTemplateService:
    """Test cases for TemplateService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.template_service import TemplateService
        
        mock_db = MagicMock()
        service = TemplateService(mock_db)
        assert service is not None
        assert service.db == mock_db


class TestSecurityService:
    """Test cases for SecurityService."""
    
    def test_service_initialization(self):
        """Test service initialization."""
        from src.services.security_service import SecurityService
        
        mock_db = MagicMock()
        service = SecurityService(mock_db)
        assert service is not None
        assert service.db == mock_db



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


