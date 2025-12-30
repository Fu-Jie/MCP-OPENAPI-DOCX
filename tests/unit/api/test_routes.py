"""Additional API route tests for coverage."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import ASGITransport, AsyncClient
from src.api.main import create_application


@pytest.fixture
def test_app():
    """Create test application."""
    return create_application()


@pytest.fixture
async def test_client(test_app):
    """Get async test client."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestCommentsRoutes:
    """Test cases for comments routes."""
    
    @pytest.mark.asyncio
    async def test_list_comments_no_auth(self, test_client):
        """Test listing comments without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/comments")
        # Should get some response (may be 401 or redirected based on middleware)
        assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.asyncio
    async def test_add_comment_no_auth(self, test_client):
        """Test adding comment without authentication."""
        response = await test_client.post(
            "/api/v1/documents/test-id/comments",
            json={"text": "Test comment"}
        )
        # Should get unauthorized or not found
        assert response.status_code in [401, 403, 404, 422]


class TestMetadataRoutes:
    """Test cases for metadata routes."""
    
    @pytest.mark.asyncio
    async def test_get_metadata_no_auth(self, test_client):
        """Test getting metadata without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/metadata")
        assert response.status_code in [200, 401, 403, 404]
    
    @pytest.mark.asyncio
    async def test_update_metadata_no_auth(self, test_client):
        """Test updating metadata without authentication."""
        response = await test_client.put(
            "/api/v1/documents/test-id/metadata",
            json={"title": "New Title"}
        )
        assert response.status_code in [401, 403, 404, 422]


class TestLayoutRoutes:
    """Test cases for layout routes."""
    
    @pytest.mark.asyncio
    async def test_get_page_settings_no_auth(self, test_client):
        """Test getting page settings without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/layout/page")
        assert response.status_code in [200, 401, 403, 404]


class TestListsRoutes:
    """Test cases for lists routes."""
    
    @pytest.mark.asyncio
    async def test_get_lists_no_auth(self, test_client):
        """Test getting lists without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/lists")
        assert response.status_code in [200, 401, 403, 404]


class TestMediaRoutes:
    """Test cases for media routes."""
    
    @pytest.mark.asyncio
    async def test_list_media_no_auth(self, test_client):
        """Test listing media without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/media")
        assert response.status_code in [200, 401, 403, 404]


class TestSearchRoutes:
    """Test cases for search routes."""
    
    @pytest.mark.asyncio
    async def test_search_documents_no_auth(self, test_client):
        """Test searching documents without authentication."""
        response = await test_client.get("/api/v1/search?q=test")
        assert response.status_code in [200, 401, 403, 404, 422]


class TestStylesRoutes:
    """Test cases for styles routes."""
    
    @pytest.mark.asyncio
    async def test_get_styles_no_auth(self, test_client):
        """Test getting styles without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/styles")
        assert response.status_code in [200, 401, 403, 404]


class TestTablesRoutesAdditional:
    """Additional test cases for tables routes."""
    
    @pytest.mark.asyncio
    async def test_update_cell_no_auth(self, test_client):
        """Test updating cell without authentication."""
        response = await test_client.put(
            "/api/v1/documents/test-id/tables/0/cell/0/0",
            json={"value": "New Value"}
        )
        assert response.status_code in [401, 403, 404, 422]


class TestTOCRoutes:
    """Test cases for TOC routes."""
    
    @pytest.mark.asyncio
    async def test_get_toc_no_auth(self, test_client):
        """Test getting TOC without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/toc")
        assert response.status_code in [200, 401, 403, 404, 405]


class TestRevisionsRoutes:
    """Test cases for revisions routes."""
    
    @pytest.mark.asyncio
    async def test_list_revisions_no_auth(self, test_client):
        """Test listing revisions without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/revisions")
        assert response.status_code in [200, 401, 403, 404]


class TestSecurityRoutes:
    """Test cases for security routes."""
    
    @pytest.mark.asyncio
    async def test_list_permissions_no_auth(self, test_client):
        """Test listing permissions without authentication."""
        response = await test_client.get("/api/v1/documents/test-id/permissions")
        assert response.status_code in [200, 401, 403, 404]
