"""MCP Server main module.

This module implements the MCP (Model Context Protocol) server
for document operations, allowing AI assistants to interact
with DOCX documents.
"""

import asyncio
import logging
from typing import Any

from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    TextContent,
    Tool,
)

from mcp.server import Server
from src.core.config import get_settings
from src.mcp.handlers import MCPHandler
from src.mcp.resources import register_resources
from src.mcp.tools import register_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
mcp_server = Server("docx-mcp-server")

# Initialize handler
handler = MCPHandler()


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools.

    Returns:
        List of Tool definitions.
    """
    return register_tools()


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle MCP tool calls.

    Args:
        name: Tool name.
        arguments: Tool arguments.

    Returns:
        List of TextContent with tool results.
    """
    try:
        result = await handler.execute_tool(name, arguments)
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


@mcp_server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available MCP resources.

    Returns:
        List of Resource definitions.
    """
    return register_resources()


@mcp_server.read_resource()
async def read_resource(uri: str) -> str:
    """Read an MCP resource.

    Args:
        uri: Resource URI.

    Returns:
        Resource content as string.
    """
    try:
        return await handler.read_resource(uri)
    except Exception as e:
        logger.error(f"Resource read error: {e}")
        return f"Error: {str(e)}"


async def run_server() -> None:
    """Run the MCP server."""
    settings = get_settings()
    logger.info(f"Starting MCP server: {settings.mcp_server_name}")

    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options(),
        )


def main() -> None:
    """Main entry point for MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
