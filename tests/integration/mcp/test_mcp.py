"""Integration tests for MCP server."""

import pytest


class TestMCPTools:
    """Test cases for MCP tools."""

    def test_tools_registry_exists(self):
        """Test that tools registry is properly set up."""
        from src.mcp.tools import register_tools

        tools = register_tools()
        assert tools is not None
        assert isinstance(tools, list)
        assert len(tools) > 0

    def test_document_tools_defined(self):
        """Test that document tools are defined."""
        from src.mcp.tools import register_tools

        tools = register_tools()
        # Check for some expected tools
        tool_names = [t.name for t in tools]
        assert len(tool_names) > 0

        # Should have document-related tools
        doc_tools = [t for t in tool_names if "document" in t.lower()]
        assert len(doc_tools) > 0

    def test_tool_has_description(self):
        """Test that tools have descriptions."""
        from src.mcp.tools import register_tools

        tools = register_tools()
        for tool in tools:
            assert tool.description is not None, f"Tool {tool.name} missing description"
            assert len(tool.description) > 0


class TestMCPResources:
    """Test cases for MCP resources."""

    def test_resources_list(self):
        """Test that resources are defined."""
        from src.mcp.resources import register_resources

        resources = register_resources()
        assert resources is not None
        assert isinstance(resources, list)


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

        # First create a document so we can get info about it
        await handler.execute_tool(
            name="create_document",
            arguments={"title": "Test Document"}
        )

        # Test getting document info
        result = await handler.execute_tool(
            name="get_document_info",
            arguments={}
        )

        assert result is not None
        assert "paragraphs" in result or "error" not in result
