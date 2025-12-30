#!/usr/bin/env python3
"""Run the application server.

This script starts the FastAPI application server.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main() -> None:
    """Run the application."""
    from src.api.main import run
    run()


if __name__ == "__main__":
    main()
