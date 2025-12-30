"""Integration tests for MCP server."""

import pytest
from unittest.mock import MagicMock, patch


class TestMCPTools:
    """Test cases for MCP tools."""

    def test_tools_registry_exists(self):
        """Test that tools registry is properly set up."""
        from src.mcp.tools import TOOLS

        assert TOOLS is not None
        assert isinstance(TOOLS, dict)
        assert len(TOOLS) > 0

    def test_document_tools_defined(self):
        """Test that document tools are defined."""
        from src.mcp.tools import TOOLS

        # Check for some expected tools
        tool_names = list(TOOLS.keys())
        assert len(tool_names) > 0

        # Should have document-related tools
        doc_tools = [t for t in tool_names if "document" in t.lower()]
        assert len(doc_tools) > 0

    def test_tool_has_description(self):
        """Test that tools have descriptions."""
        from src.mcp.tools import TOOLS

        for name, tool in TOOLS.items():
            assert "description" in tool, f"Tool {name} missing description"
            assert len(tool["description"]) > 0


class TestMCPResources:
    """Test cases for MCP resources."""

    def test_resources_list(self):
        """Test that resources are defined."""
        from src.mcp.resources import RESOURCES

        assert RESOURCES is not None
        assert isinstance(RESOURCES, list)


class TestMCPHandlers:
    """Test cases for MCP handlers."""

    def test_handler_initialization(self):
        """Test handler can be initialized."""
        from src.mcp.handlers import MCPHandler

        handler = MCPHandler()
        assert handler is not None

    @pytest.mark.asyncio
    async def test_handle_tool_call(self):
        """Test handling a tool call."""
        from src.mcp.handlers import MCPHandler

        handler = MCPHandler()

        # Test with a simple tool
        result = await handler.handle_tool_call(
            tool_name="get_document_info",
            arguments={"document_id": "test-123"}
        )

        assert result is not None
