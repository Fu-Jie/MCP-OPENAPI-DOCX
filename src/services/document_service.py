"""Document service for CRUD and management operations.

This module provides the DocumentService class which handles all
document-related business logic including creation, reading, updating,
and deleting documents.
"""

import os
import uuid
from datetime import datetime
from typing import Any, BinaryIO

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload

from src.core.config import get_settings
from src.core.exceptions import (
    DocumentNotFoundError,
    DocumentProcessingError,
    ValidationError,
)
from src.handlers.document_handler import DocumentHandler
from src.models.database import Document, DocumentVersion
from src.models.dto import DocumentDTO


class DocumentService:
    """Service class for document operations.

    This service provides methods for document CRUD operations,
    version management, and document processing.

    Attributes:
        db: Database session for persistence operations.
        document_handler: Handler for DOCX file operations.
        settings: Application settings.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the document service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.settings = get_settings()

    async def create_document(
        self,
        name: str,
        user_id: str,
        content: bytes | None = None,
        template_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentDTO:
        """Create a new document.

        Args:
            name: Document name.
            user_id: ID of the user creating the document.
            content: Optional initial content (DOCX bytes).
            template_id: Optional template ID to use.
            metadata: Optional document metadata.

        Returns:
            Created document DTO.

        Raises:
            ValidationError: If validation fails.
            DocumentProcessingError: If document creation fails.
        """
        try:
            # Generate document ID
            doc_id = str(uuid.uuid4())

            # Create document file
            if content:
                file_path = await self._save_document_file(doc_id, content)
                doc = self.document_handler.load_document(file_path)
            elif template_id:
                # Load from template
                file_path = await self._create_from_template(doc_id, template_id)
                doc = self.document_handler.load_document(file_path)
            else:
                # Create empty document
                file_path = await self._create_empty_document(doc_id)
                doc = self.document_handler.create_document()
                self.document_handler.save_document(doc, file_path)

            # Extract metadata
            doc_metadata = self.document_handler.get_metadata(doc)
            if metadata:
                doc_metadata.update(metadata)

            # Create database record
            document = Document(
                id=doc_id,
                name=name,
                file_path=file_path,
                user_id=user_id,
                metadata=doc_metadata,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )

            self.db.add(document)

            # Create initial version
            version = DocumentVersion(
                id=str(uuid.uuid4()),
                document_id=doc_id,
                version_number=1,
                file_path=file_path,
                created_by=user_id,
                created_at=datetime.utcnow(),
                comment="Initial version",
            )
            self.db.add(version)

            await self.db.commit()
            await self.db.refresh(document)

            return DocumentDTO.from_orm(document)

        except Exception as e:
            await self.db.rollback()
            raise DocumentProcessingError(f"Failed to create document: {str(e)}")

    async def get_document(self, document_id: str) -> DocumentDTO:
        """Get a document by ID.

        Args:
            document_id: Document ID.

        Returns:
            Document DTO.

        Raises:
            DocumentNotFoundError: If document not found.
        """
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Document {document_id} not found")

        return DocumentDTO.from_orm(document)

    async def update_document(
        self,
        document_id: str,
        name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentDTO:
        """Update document metadata.

        Args:
            document_id: Document ID.
            name: Optional new name.
            metadata: Optional updated metadata.

        Returns:
            Updated document DTO.

        Raises:
            DocumentNotFoundError: If document not found.
        """
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Document {document_id} not found")

        if name:
            document.name = name
        if metadata:
            existing_metadata = document.metadata or {}
            existing_metadata.update(metadata)
            document.metadata = existing_metadata

        document.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(document)

        return DocumentDTO.from_orm(document)

    async def delete_document(self, document_id: str) -> bool:
        """Delete a document.

        Args:
            document_id: Document ID.

        Returns:
            True if deleted successfully.

        Raises:
            DocumentNotFoundError: If document not found.
        """
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Document {document_id} not found")

        # Delete file
        if document.file_path and os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Delete versions
        await self.db.execute(
            delete(DocumentVersion).where(
                DocumentVersion.document_id == document_id
            )
        )

        # Delete document
        await self.db.execute(
            delete(Document).where(Document.id == document_id)
        )

        await self.db.commit()
        return True

    async def list_documents(
        self,
        user_id: str | None = None,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> tuple[list[DocumentDTO], int]:
        """List documents with pagination.

        Args:
            user_id: Optional user ID filter.
            skip: Number of records to skip.
            limit: Maximum records to return.
            search: Optional search query.

        Returns:
            Tuple of (documents list, total count).
        """
        query = select(Document)

        if user_id:
            query = query.where(Document.user_id == user_id)

        if search:
            query = query.where(Document.name.ilike(f"%{search}%"))

        # Get total count
        count_query = select(Document.id)
        if user_id:
            count_query = count_query.where(Document.user_id == user_id)
        if search:
            count_query = count_query.where(Document.name.ilike(f"%{search}%"))

        count_result = await self.db.execute(count_query)
        total = len(count_result.all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Document.updated_at.desc())
        result = await self.db.execute(query)
        documents = result.scalars().all()

        return [DocumentDTO.from_orm(doc) for doc in documents], total

    async def get_document_content(self, document_id: str) -> bytes:
        """Get document file content.

        Args:
            document_id: Document ID.

        Returns:
            Document file bytes.

        Raises:
            DocumentNotFoundError: If document not found.
        """
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Document {document_id} not found")

        if not document.file_path or not os.path.exists(document.file_path):
            raise DocumentProcessingError("Document file not found on disk")

        with open(document.file_path, "rb") as f:
            return f.read()

    async def update_document_content(
        self,
        document_id: str,
        content: bytes,
        user_id: str,
        comment: str | None = None,
    ) -> DocumentDTO:
        """Update document content and create new version.

        Args:
            document_id: Document ID.
            content: New document content.
            user_id: User making the update.
            comment: Optional version comment.

        Returns:
            Updated document DTO.

        Raises:
            DocumentNotFoundError: If document not found.
            DocumentProcessingError: If update fails.
        """
        result = await self.db.execute(
            select(Document)
            .options(selectinload(Document.versions))
            .where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Document {document_id} not found")

        try:
            # Save new content
            file_path = document.file_path
            with open(file_path, "wb") as f:
                f.write(content)

            # Get new version number
            current_version = max(
                (v.version_number for v in document.versions), default=0
            )
            new_version = current_version + 1

            # Create version record
            version = DocumentVersion(
                id=str(uuid.uuid4()),
                document_id=document_id,
                version_number=new_version,
                file_path=file_path,
                created_by=user_id,
                created_at=datetime.utcnow(),
                comment=comment or f"Version {new_version}",
            )
            self.db.add(version)

            document.updated_at = datetime.utcnow()
            document.current_version = new_version

            await self.db.commit()
            await self.db.refresh(document)

            return DocumentDTO.from_orm(document)

        except Exception as e:
            await self.db.rollback()
            raise DocumentProcessingError(f"Failed to update document: {str(e)}")

    async def _save_document_file(self, doc_id: str, content: bytes) -> str:
        """Save document content to file.

        Args:
            doc_id: Document ID.
            content: File content.

        Returns:
            File path.
        """
        file_path = os.path.join(self.settings.upload_dir, f"{doc_id}.docx")
        with open(file_path, "wb") as f:
            f.write(content)
        return file_path

    async def _create_empty_document(self, doc_id: str) -> str:
        """Create an empty document file.

        Args:
            doc_id: Document ID.

        Returns:
            File path.
        """
        file_path = os.path.join(self.settings.upload_dir, f"{doc_id}.docx")
        return file_path

    async def _create_from_template(
        self,
        doc_id: str,
        template_id: str,
    ) -> str:
        """Create document from template.

        Args:
            doc_id: Document ID.
            template_id: Template ID.

        Returns:
            File path.
        """
        # TODO: Implement template loading
        return await self._create_empty_document(doc_id)
