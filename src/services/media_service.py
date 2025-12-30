"""Media service for image and multimedia operations.

This module provides the MediaService class for handling
images and other media in documents.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import DocumentProcessingError
from src.handlers.document_handler import DocumentHandler
from src.handlers.media_handler import MediaHandler


class MediaService:
    """Service class for media operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        media_handler: Handler for media operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the media service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.media_handler = MediaHandler()

    async def insert_image(
        self,
        document_path: str,
        image_path: str,
        width: float | None = None,
        height: float | None = None,
        paragraph_index: int | None = None,
    ) -> dict[str, Any]:
        """Insert an image into the document.

        Args:
            document_path: Path to the document.
            image_path: Path to the image file.
            width: Optional width in inches.
            height: Optional height in inches.
            paragraph_index: Optional position to insert.

        Returns:
            Result with image details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.media_handler.insert_image(
                doc, image_path, width, height, paragraph_index
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "image": image_path}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to insert image: {str(e)}")

    async def insert_image_from_bytes(
        self,
        document_path: str,
        image_data: bytes,
        filename: str,
        width: float | None = None,
        height: float | None = None,
    ) -> dict[str, Any]:
        """Insert an image from bytes.

        Args:
            document_path: Path to the document.
            image_data: Image bytes.
            filename: Image filename.
            width: Optional width in inches.
            height: Optional height in inches.

        Returns:
            Result with image details.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.media_handler.insert_image_from_bytes(
                doc, image_data, filename, width, height
            )
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "filename": filename}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to insert image: {str(e)}")

    async def get_images(
        self,
        document_path: str,
    ) -> list[dict[str, Any]]:
        """Get all images from the document.

        Args:
            document_path: Path to the document.

        Returns:
            List of image information.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.media_handler.get_images(doc)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to get images: {str(e)}")

    async def extract_image(
        self,
        document_path: str,
        image_index: int,
    ) -> bytes:
        """Extract an image from the document.

        Args:
            document_path: Path to the document.
            image_index: Index of the image.

        Returns:
            Image bytes.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            return self.media_handler.extract_image(doc, image_index)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to extract image: {str(e)}")

    async def resize_image(
        self,
        document_path: str,
        image_index: int,
        width: float | None = None,
        height: float | None = None,
    ) -> dict[str, Any]:
        """Resize an image in the document.

        Args:
            document_path: Path to the document.
            image_index: Index of the image.
            width: New width in inches.
            height: New height in inches.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.media_handler.resize_image(doc, image_index, width, height)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "width": width, "height": height}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to resize image: {str(e)}")

    async def delete_image(
        self,
        document_path: str,
        image_index: int,
    ) -> dict[str, Any]:
        """Delete an image from the document.

        Args:
            document_path: Path to the document.
            image_index: Index of the image to delete.

        Returns:
            Result indicating success.
        """
        try:
            doc = self.document_handler.load_document(document_path)
            self.media_handler.delete_image(doc, image_index)
            self.document_handler.save_document(doc, document_path)
            return {"success": True, "deleted_index": image_index}
        except Exception as e:
            raise DocumentProcessingError(f"Failed to delete image: {str(e)}")
