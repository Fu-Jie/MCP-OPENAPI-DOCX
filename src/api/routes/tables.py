"""Table routes.

This module provides endpoints for table operations.
"""

import os
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.table_handler import TableHandler
from src.models.schemas import TableCreate

router = APIRouter(prefix="/documents/{document_id}/tables")


def get_table_handler(document_id: str) -> tuple[DocumentHandler, TableHandler]:
    """Get table handler for a document.

    Args:
        document_id: Document UUID.

    Returns:
        Tuple of (DocumentHandler, TableHandler).

    Raises:
        DocumentNotFoundError: If document not found.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    return doc_handler, TableHandler(doc_handler.document)


@router.get(
    "",
    summary="Get All Tables",
    description="Get all tables in the document.",
)
async def get_tables(document_id: str) -> dict[str, Any]:
    """Get all tables.

    Args:
        document_id: Document UUID.

    Returns:
        List of tables.
    """
    _, handler = get_table_handler(document_id)
    tables = handler.get_all_tables()

    return {
        "document_id": document_id,
        "count": len(tables),
        "tables": [
            {
                "index": t.index,
                "rows": t.rows,
                "cols": t.cols,
                "style": t.style,
            }
            for t in tables
        ],
    }


@router.get(
    "/{index}",
    summary="Get Table",
    description="Get a specific table by index.",
)
async def get_table(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Get a table by index.

    Args:
        document_id: Document UUID.
        index: Table index.

    Returns:
        Table information.
    """
    _, handler = get_table_handler(document_id)
    table = handler.get_table(index)

    return {
        "index": table.index,
        "rows": table.rows,
        "cols": table.cols,
        "style": table.style,
        "data": handler.get_table_as_list(index),
    }


@router.post(
    "",
    summary="Add Table",
    description="Add a new table to the document.",
)
async def add_table(
    document_id: str,
    data: TableCreate,
) -> dict[str, Any]:
    """Add a new table.

    Args:
        document_id: Document UUID.
        data: Table creation data.

    Returns:
        Created table information.
    """
    doc_handler, handler = get_table_handler(document_id)

    # Convert data rows to simple list
    table_data = None
    if data.data:
        table_data = [
            [cell.text for cell in row.cells]
            for row in data.data
        ]

    index = handler.add_table(
        rows=data.rows,
        cols=data.cols,
        style=data.style,
        data=table_data,
    )

    doc_handler.save_document()

    return {
        "index": index,
        "rows": data.rows,
        "cols": data.cols,
        "style": data.style,
    }


@router.delete(
    "/{index}",
    summary="Delete Table",
    description="Delete a table.",
)
async def delete_table(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Delete a table.

    Args:
        document_id: Document UUID.
        index: Table index.

    Returns:
        Deletion confirmation.
    """
    doc_handler, handler = get_table_handler(document_id)
    handler.delete_table(index)
    doc_handler.save_document()

    return {"deleted": True, "index": index}


@router.get(
    "/{table_index}/cells/{row}/{col}",
    summary="Get Cell",
    description="Get a specific cell from a table.",
)
async def get_cell(
    document_id: str,
    table_index: int,
    row: int,
    col: int,
) -> dict[str, Any]:
    """Get a table cell.

    Args:
        document_id: Document UUID.
        table_index: Table index.
        row: Row index.
        col: Column index.

    Returns:
        Cell information.
    """
    _, handler = get_table_handler(document_id)
    cell = handler.get_cell(table_index, row, col)

    return {
        "row": cell.row,
        "col": cell.col,
        "text": cell.text,
    }


@router.put(
    "/{table_index}/cells/{row}/{col}",
    summary="Update Cell",
    description="Update a specific cell in a table.",
)
async def update_cell(
    document_id: str,
    table_index: int,
    row: int,
    col: int,
    text: str,
) -> dict[str, Any]:
    """Update a table cell.

    Args:
        document_id: Document UUID.
        table_index: Table index.
        row: Row index.
        col: Column index.
        text: New cell text.

    Returns:
        Updated cell information.
    """
    doc_handler, handler = get_table_handler(document_id)
    cell = handler.set_cell(table_index, row, col, text)
    doc_handler.save_document()

    return {
        "row": cell.row,
        "col": cell.col,
        "text": cell.text,
        "updated": True,
    }


@router.post(
    "/{index}/rows",
    summary="Add Row",
    description="Add a row to a table.",
)
async def add_row(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Add a row to a table.

    Args:
        document_id: Document UUID.
        index: Table index.

    Returns:
        New row information.
    """
    doc_handler, handler = get_table_handler(document_id)
    row_index = handler.add_row(index)
    doc_handler.save_document()

    return {"table_index": index, "row_index": row_index}


@router.post(
    "/{index}/columns",
    summary="Add Column",
    description="Add a column to a table.",
)
async def add_column(
    document_id: str,
    index: int,
) -> dict[str, Any]:
    """Add a column to a table.

    Args:
        document_id: Document UUID.
        index: Table index.

    Returns:
        New column information.
    """
    doc_handler, handler = get_table_handler(document_id)
    col_index = handler.add_column(index)
    doc_handler.save_document()

    return {"table_index": index, "col_index": col_index}


@router.delete(
    "/{table_index}/rows/{row_index}",
    summary="Delete Row",
    description="Delete a row from a table.",
)
async def delete_row(
    document_id: str,
    table_index: int,
    row_index: int,
) -> dict[str, Any]:
    """Delete a row from a table.

    Args:
        document_id: Document UUID.
        table_index: Table index.
        row_index: Row index.

    Returns:
        Deletion confirmation.
    """
    doc_handler, handler = get_table_handler(document_id)
    handler.delete_row(table_index, row_index)
    doc_handler.save_document()

    return {"deleted": True, "table_index": table_index, "row_index": row_index}


@router.post(
    "/{table_index}/merge",
    summary="Merge Cells",
    description="Merge a range of cells.",
)
async def merge_cells(
    document_id: str,
    table_index: int,
    start_row: int,
    start_col: int,
    end_row: int,
    end_col: int,
) -> dict[str, Any]:
    """Merge cells in a table.

    Args:
        document_id: Document UUID.
        table_index: Table index.
        start_row: Starting row.
        start_col: Starting column.
        end_row: Ending row.
        end_col: Ending column.

    Returns:
        Merge confirmation.
    """
    doc_handler, handler = get_table_handler(document_id)
    handler.merge_cells(table_index, start_row, start_col, end_row, end_col)
    doc_handler.save_document()

    return {
        "merged": True,
        "range": {
            "start_row": start_row,
            "start_col": start_col,
            "end_row": end_row,
            "end_col": end_col,
        },
    }
