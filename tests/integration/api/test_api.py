"""Integration tests for API endpoints."""

import pytest
from httpx import AsyncClient


class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check returns OK."""
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_health_check_detailed(self, client: AsyncClient):
        """Test detailed health check."""
        response = await client.get("/api/v1/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestRootEndpoint:
    """Test cases for root endpoint."""

    @pytest.mark.asyncio
    async def test_root(self, client: AsyncClient):
        """Test root endpoint returns API info."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data


class TestDocumentsEndpoint:
    """Test cases for documents endpoints."""

    @pytest.mark.asyncio
    async def test_list_documents(self, client: AsyncClient):
        """Test listing documents."""
        response = await client.get("/api/v1/documents")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or isinstance(data, list)

    @pytest.mark.asyncio
    async def test_create_document_no_auth(self, client: AsyncClient):
        """Test creating document without auth."""
        response = await client.post(
            "/api/v1/documents",
            json={"name": "Test Document"}
        )
        # Should work or return 401 depending on auth config
        assert response.status_code in [200, 201, 401, 422]

    @pytest.mark.asyncio
    async def test_get_document_not_found(self, client: AsyncClient):
        """Test getting non-existent document."""
        response = await client.get("/api/v1/documents/non-existent-id")
        assert response.status_code == 404


class TestTemplatesEndpoint:
    """Test cases for templates endpoints."""

    @pytest.mark.asyncio
    async def test_list_templates(self, client: AsyncClient):
        """Test listing templates."""
        response = await client.get("/api/v1/templates")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_get_categories(self, client: AsyncClient):
        """Test getting template categories."""
        response = await client.get("/api/v1/templates/categories")
        assert response.status_code == 200
