"""Unit tests for table handler."""

import pytest
from docx import Document

from src.handlers.table_handler import TableHandler


class TestTableHandler:
    """Test cases for TableHandler class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.doc = Document()
        self.handler = TableHandler(self.doc)

    def test_add_table(self):
        """Test creating a table."""
        index = self.handler.add_table(rows=3, cols=3)
        assert index == 0
        assert len(self.doc.tables) == 1
        assert len(self.doc.tables[0].rows) == 3

    def test_add_table_with_data(self):
        """Test creating a table with data."""
        data = [
            ["A1", "B1", "C1"],
            ["A2", "B2", "C2"],
        ]
        index = self.handler.add_table(rows=2, cols=3, data=data)

        assert self.doc.tables[index].cell(0, 0).text == "A1"
        assert self.doc.tables[index].cell(0, 2).text == "C1"
        assert self.doc.tables[index].cell(1, 1).text == "B2"

    def test_get_table(self):
        """Test getting table data."""
        data = [["R1C1", "R1C2"], ["R2C1", "R2C2"]]
        self.handler.add_table(rows=2, cols=2, data=data)

        table_dto = self.handler.get_table(0)
        assert table_dto.rows == 2
        assert table_dto.cols == 2

    def test_set_cell(self):
        """Test updating a cell value."""
        self.handler.add_table(rows=2, cols=2)
        self.handler.set_cell(0, row=0, col=0, text="Updated")

        table_dto = self.handler.get_table(0)
        assert table_dto.cells[0][0].text == "Updated"

    def test_add_row(self):
        """Test adding a row to a table."""
        self.handler.add_table(rows=2, cols=2)
        self.handler.add_row(0)

        table_dto = self.handler.get_table(0)
        assert table_dto.rows == 3

    def test_get_all_tables(self):
        """Test listing all tables."""
        self.handler.add_table(rows=2, cols=2)
        self.handler.add_table(rows=3, cols=3)

        tables = self.handler.get_all_tables()
        assert len(tables) == 2
        assert tables[0].rows == 2
        assert tables[1].rows == 3
