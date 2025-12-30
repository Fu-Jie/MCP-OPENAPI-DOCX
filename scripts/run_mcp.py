#!/usr/bin/env python3
"""Run the MCP server.

This script starts the MCP (Model Context Protocol) server.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main() -> None:
    """Run the MCP server."""
    from src.mcp.server import main as mcp_main
    mcp_main()


if __name__ == "__main__":
    main()
