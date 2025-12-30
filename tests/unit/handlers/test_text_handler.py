"""Unit tests for text handler."""

import pytest
from docx import Document

from src.handlers.text_handler import TextHandler


class TestTextHandler:
    """Test cases for TextHandler class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.doc = Document()
        self.handler = TextHandler(self.doc)

    def test_add_paragraph(self):
        """Test adding a paragraph."""
        index = self.handler.add_paragraph("Test paragraph")
        assert index == 0
        assert len(self.doc.paragraphs) == 1
        assert self.doc.paragraphs[0].text == "Test paragraph"

    def test_add_paragraph_with_style(self):
        """Test adding a paragraph with style."""
        index = self.handler.add_paragraph("Heading text", style="Heading 1")
        assert index >= 0
        para = self.doc.paragraphs[index]
        assert para.text == "Heading text"

    def test_get_all_paragraphs(self):
        """Test getting paragraphs."""
        self.handler.add_paragraph("Para 1")
        self.handler.add_paragraph("Para 2")

        paragraphs = self.handler.get_all_paragraphs()
        assert len(paragraphs) == 2
        assert paragraphs[0].text == "Para 1"
        assert paragraphs[1].text == "Para 2"

    def test_get_paragraph(self):
        """Test getting a single paragraph."""
        self.handler.add_paragraph("Test paragraph")
        para = self.handler.get_paragraph(0)
        assert para.text == "Test paragraph"

    def test_find_text(self):
        """Test searching for text."""
        self.handler.add_paragraph("Hello world")
        self.handler.add_paragraph("World is beautiful")
        self.handler.add_paragraph("Hello again")

        results = self.handler.find_text("world")
        assert len(results) >= 1

    def test_replace_text(self):
        """Test replacing text."""
        self.handler.add_paragraph("Hello world")
        self.handler.add_paragraph("world is great")

        count = self.handler.replace_text(find="world", replace="universe")
        assert count >= 1

        paragraphs = self.handler.get_all_paragraphs()
        found_universe = False
        for p in paragraphs:
            if "universe" in p.text:
                found_universe = True
                break
        assert found_universe
