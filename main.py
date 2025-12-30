#!/usr/bin/env python3
"""
MCP-OPENAPI-DOCX Main Entry Point.

This is the main entry point for the application.
Run this file directly to start the API server.

Usage:
    python main.py [--mcp]

Options:
    --mcp    Start the MCP server instead of the API server
"""

import argparse
import sys
from pathlib import Path

# Ensure the project root is in the path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def run_api_server() -> None:
    """Start the FastAPI application server."""
    import uvicorn
    from src.core.config import get_settings
    
    settings = get_settings()
    
    uvicorn.run(
        "src.api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
    )


def run_mcp_server() -> None:
    """Start the MCP server."""
    from src.mcp.server import main as mcp_main
    mcp_main()


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="MCP-OPENAPI-DOCX Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py              # Start API server
    python main.py --mcp        # Start MCP server
        """
    )
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="Start the MCP server instead of the API server"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=None,
        help="Host to bind to (overrides config)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind to (overrides config)"
    )
    
    args = parser.parse_args()
    
    # Set environment variables if provided
    import os
    if args.host:
        os.environ["HOST"] = args.host
    if args.port:
        os.environ["PORT"] = str(args.port)
    
    if args.mcp:
        print("Starting MCP Server...")
        run_mcp_server()
    else:
        print("Starting API Server...")
        run_api_server()


if __name__ == "__main__":
    main()
