"""Conversion utility functions.

This module provides conversion utilities for transforming
data between different formats.
"""

from typing import Any
from docx.shared import Inches, Pt, Cm, Emu, Twips


class ConversionUtils:
    """Utility class for unit conversions.

    Provides static methods for converting between various units
    used in document processing.
    """

    # Conversion constants
    INCHES_PER_CM = 0.393701
    CM_PER_INCH = 2.54
    POINTS_PER_INCH = 72
    EMU_PER_INCH = 914400
    TWIPS_PER_INCH = 1440

    @staticmethod
    def inches_to_cm(inches: float) -> float:
        """Convert inches to centimeters.

        Args:
            inches: Value in inches.

        Returns:
            Value in centimeters.
        """
        return inches * ConversionUtils.CM_PER_INCH

    @staticmethod
    def cm_to_inches(cm: float) -> float:
        """Convert centimeters to inches.

        Args:
            cm: Value in centimeters.

        Returns:
            Value in inches.
        """
        return cm * ConversionUtils.INCHES_PER_CM

    @staticmethod
    def points_to_inches(points: float) -> float:
        """Convert points to inches.

        Args:
            points: Value in points.

        Returns:
            Value in inches.
        """
        return points / ConversionUtils.POINTS_PER_INCH

    @staticmethod
    def inches_to_points(inches: float) -> float:
        """Convert inches to points.

        Args:
            inches: Value in inches.

        Returns:
            Value in points.
        """
        return inches * ConversionUtils.POINTS_PER_INCH

    @staticmethod
    def emu_to_inches(emu: int) -> float:
        """Convert EMUs to inches.

        Args:
            emu: Value in EMUs.

        Returns:
            Value in inches.
        """
        return emu / ConversionUtils.EMU_PER_INCH

    @staticmethod
    def inches_to_emu(inches: float) -> int:
        """Convert inches to EMUs.

        Args:
            inches: Value in inches.

        Returns:
            Value in EMUs.
        """
        return int(inches * ConversionUtils.EMU_PER_INCH)

    @staticmethod
    def twips_to_inches(twips: int) -> float:
        """Convert twips to inches.

        Args:
            twips: Value in twips.

        Returns:
            Value in inches.
        """
        return twips / ConversionUtils.TWIPS_PER_INCH

    @staticmethod
    def inches_to_twips(inches: float) -> int:
        """Convert inches to twips.

        Args:
            inches: Value in inches.

        Returns:
            Value in twips.
        """
        return int(inches * ConversionUtils.TWIPS_PER_INCH)

    @staticmethod
    def to_docx_inches(value: float) -> Inches:
        """Convert to python-docx Inches object.

        Args:
            value: Value in inches.

        Returns:
            Inches object.
        """
        return Inches(value)

    @staticmethod
    def to_docx_pt(value: float) -> Pt:
        """Convert to python-docx Pt object.

        Args:
            value: Value in points.

        Returns:
            Pt object.
        """
        return Pt(value)

    @staticmethod
    def to_docx_cm(value: float) -> Cm:
        """Convert to python-docx Cm object.

        Args:
            value: Value in centimeters.

        Returns:
            Cm object.
        """
        return Cm(value)

    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
        """Convert hex color to RGB.

        Args:
            hex_color: Hex color string (with or without #).

        Returns:
            Tuple of (r, g, b) values.
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    @staticmethod
    def rgb_to_hex(r: int, g: int, b: int) -> str:
        """Convert RGB to hex color.

        Args:
            r: Red value (0-255).
            g: Green value (0-255).
            b: Blue value (0-255).

        Returns:
            Hex color string.
        """
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def bytes_to_human_readable(size: int) -> str:
        """Convert bytes to human-readable size.

        Args:
            size: Size in bytes.

        Returns:
            Human-readable size string.
        """
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    @staticmethod
    def parse_size(size_str: str) -> int:
        """Parse human-readable size to bytes.

        Args:
            size_str: Size string (e.g., "10MB").

        Returns:
            Size in bytes.
        """
        size_str = size_str.strip().upper()
        units = {
            "B": 1,
            "KB": 1024,
            "MB": 1024 ** 2,
            "GB": 1024 ** 3,
            "TB": 1024 ** 4,
        }
        for unit, multiplier in units.items():
            if size_str.endswith(unit):
                num = size_str[:-len(unit)].strip()
                return int(float(num) * multiplier)
        return int(size_str)

    @staticmethod
    def dict_to_xml_safe(data: dict[str, Any]) -> dict[str, str]:
        """Convert dict values to XML-safe strings.

        Args:
            data: Input dictionary.

        Returns:
            Dictionary with string values.
        """
        result = {}
        for key, value in data.items():
            if value is None:
                result[key] = ""
            elif isinstance(value, bool):
                result[key] = "true" if value else "false"
            else:
                result[key] = str(value)
        return result
