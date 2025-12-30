"""Table service for table operations.

This module provides the TableService class for table
creation, modification, and data management.
"""

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.handlers.document_handler import DocumentHandler
from src.handlers.table_handler import TableHandler
from src.core.exceptions import DocumentProcessingError


class TableService:
    """Service class for table operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        table_handler: Handler for table operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the table service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.table_handler = TableHandler()

    async def create_table(
        self,
        document_path: str,
        rows: int,
        cols: int,
        data: list[list[str]] | None = None,
        style: str | None = None,
    ) -> dict[str, Any]:
        """Create a new table.

        Args:
            document_path: Path to the document.
            rows: Number of rows.
            cols: Number of columns.
            data: Optional table data.
            style: Optional table style.

        Returns:
            Result with table details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            table = self.table_handler.create_table(doc, rows, cols, data, style)
            self.document_handler.save_document(doc, document_path)
            return {
                "success": True,
                "rows": rows,
                "cols": cols,
                "table_index": len(doc.tables) - 1,
            }
        except Exception as e:
            raise DocumentProcessingError(f"Failed to create table: {str(e)}")

    async def get_table(
        self,
        document_path: str,
        table_index: int,
    ) -> dict[str, Any]:
        """Get table data.

        Args:
            document_path: Path to the document.
            table_index: Index of the table.

        Returns:
            Table data.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.table_handler.get_table_data(doc, table_index)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get table: {str(e)}")

    async def update_cell(
        self,
        document_path: str,
        table_index: int,
        row: int,
        col: int,
        value: str,
    ) -> dict[str, Any]:
        """Update a cell value.

        Args:
            document_path: Path to the document.
            table_index: Index of the table.
            row: Row index.
            col: Column index.
            value: New cell value.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.table_handler.update_cell(doc, table_index, row, col, value)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "row": row, "col": col, "value": value}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to update cell: {str(e)}")

    async def add_row(
        self,
        document_path: str,
        table_index: int,
        values: list[str] | None = None,
        position: int | None = None,
    ) -> dict[str, Any]:
        """Add a row to a table.

        Args:
            document_path: Path to the document.
            table_index: Index of the table.
            values: Optional row values.
            position: Optional position to insert.

        Returns:
            Result with row details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.table_handler.add_row(doc, table_index, values, position)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "table_index": table_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add row: {str(e)}")

    async def add_column(
        self,
        document_path: str,
        table_index: int,
        values: list[str] | None = None,
        position: int | None = None,
    ) -> dict[str, Any]:
        """Add a column to a table.

        Args:
            document_path: Path to the document.
            table_index: Index of the table.
            values: Optional column values.
            position: Optional position to insert.

        Returns:
            Result with column details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.table_handler.add_column(doc, table_index, values, position)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "table_index": table_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to add column: {str(e)}")

    async def delete_row(
        self,
        document_path: str,
        table_index: int,
        row_index: int,
    ) -> dict[str, Any]:
        """Delete a row from a table.

        Args:
            document_path: Path to the document.
            table_index: Index of the table.
            row_index: Index of row to delete.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.table_handler.delete_row(doc, table_index, row_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "deleted_row": row_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete row: {str(e)}")

    async def delete_column(
        self,
        document_path: str,
        table_index: int,
        col_index: int,
    ) -> dict[str, Any]:
        """Delete a column from a table.

        Args:
            document_path: Path to the document.
            table_index: Index of the table.
            col_index: Index of column to delete.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.table_handler.delete_column(doc, table_index, col_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "deleted_col": col_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete column: {str(e)}")

    async def merge_cells(
        self,
        document_path: str,
        table_index: int,
        start_row: int,
        start_col: int,
        end_row: int,
        end_col: int,
    ) -> dict[str, Any]:
        """Merge cells in a table.

        Args:
            document_path: Path to the document.
            table_index: Index of the table.
            start_row: Starting row index.
            start_col: Starting column index.
            end_row: Ending row index.
            end_col: Ending column index.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.table_handler.merge_cells(
                doc, table_index, start_row, start_col, end_row, end_col
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to merge cells: {str(e)}")

    async def list_tables(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """List all tables in document.

        Args:
            document_path: Path to the document.

        Returns:
            List of table summaries.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.table_handler.list_tables(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to list tables: {str(e)}")
