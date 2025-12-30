"""Version service for document version control.

This module provides the VersionService class for managing
document versions and history.
"""

import os
import shutil
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.models.database import Document, DocumentVersion


class VersionService:
    """Service class for version control operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        settings: Application settings.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the version service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.settings = get_settings()

    async def get_versions(
        self,
        document_id: str,
    ) -> list[dict[str, Any]]:
        """Get all versions of a document.

        Args:
            document_id: Document ID.

        Returns:
            List of version information.
        """
        result = await self.db.execute(
            select(DocumentVersion)
            .where(DocumentVersion.document_id == document_id)
            .order_by(DocumentVersion.version_number.desc())
        )
        versions = result.scalars().all()

        return [
            {
                "id": v.id,
                "version_number": v.version_number,
                "created_by": v.created_by,
                "created_at": v.created_at.isoformat() if v.created_at else None,
                "comment": v.comment,
            }
            for v in versions
        ]

    async def get_version(
        self,
        document_id: str,
        version_number: int,
    ) -> dict[str, Any]:
        """Get a specific version.

        Args:
            document_id: Document ID.
            version_number: Version number.

        Returns:
            Version information.
        """
        result = await self.db.execute(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == version_number,
            )
        )
        version = result.scalar_one_or_none()

        if not version:
            raise DocumentNotFoundError(
                f"Version {version_number} not found for document {document_id}"
            )

        return {
            "id": version.id,
            "version_number": version.version_number,
            "created_by": version.created_by,
            "created_at": version.created_at.isoformat() if version.created_at else None,
            "comment": version.comment,
        }

    async def create_version(
        self,
        document_id: str,
        user_id: str,
        comment: str | None = None,
    ) -> dict[str, Any]:
        """Create a new version.

        Args:
            document_id: Document ID.
            user_id: User creating the version.
            comment: Optional version comment.

        Returns:
            Created version information.
        """
        result = await self.db.execute(
            select(Document)
            .options(selectinload(Document.versions))
            .where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Document {document_id} not found")

        # Get next version number
        current_version = max(
            (v.version_number for v in document.versions), default=0
        )
        new_version = current_version + 1

        # Copy current file to versions
        versions_dir = os.path.join(self.settings.upload_dir, "versions", document_id)
        os.makedirs(versions_dir, exist_ok=True)
        version_path = os.path.join(versions_dir, f"v{new_version}.docx")

        if document.file_path and os.path.exists(document.file_path):
            shutil.copy2(document.file_path, version_path)

        # Create version record
        version = DocumentVersion(
            id=str(uuid.uuid4()),
            document_id=document_id,
            version_number=new_version,
            file_path=version_path,
            created_by=user_id,
            created_at=datetime.utcnow(),
            comment=comment or f"Version {new_version}",
        )
        self.db.add(version)

        document.current_version = new_version
        document.updated_at = datetime.utcnow()

        await self.db.commit()

        return {
            "id": version.id,
            "version_number": new_version,
            "created_by": user_id,
            "comment": comment,
        }

    async def restore_version(
        self,
        document_id: str,
        version_number: int,
        user_id: str,
    ) -> dict[str, Any]:
        """Restore a previous version.

        Args:
            document_id: Document ID.
            version_number: Version to restore.
            user_id: User performing the restore.

        Returns:
            Result indicating success.
        """
        result = await self.db.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()

        if not document:
            raise DocumentNotFoundError(f"Document {document_id} not found")

        # Get the version to restore
        version_result = await self.db.execute(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == version_number,
            )
        )
        version = version_result.scalar_one_or_none()

        if not version:
            raise DocumentNotFoundError(f"Version {version_number} not found")

        # Copy version file to main document
        if version.file_path and os.path.exists(version.file_path):
            shutil.copy2(version.file_path, document.file_path)

        # Create new version record for the restore
        await self.create_version(
            document_id,
            user_id,
            f"Restored from version {version_number}",
        )

        return {
            "success": True,
            "restored_version": version_number,
            "document_id": document_id,
        }

    async def compare_versions(
        self,
        document_id: str,
        version1: int,
        version2: int,
    ) -> dict[str, Any]:
        """Compare two versions.

        Args:
            document_id: Document ID.
            version1: First version number.
            version2: Second version number.

        Returns:
            Comparison result.
        """
        # Get both versions
        v1_result = await self.db.execute(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == version1,
            )
        )
        v1 = v1_result.scalar_one_or_none()

        v2_result = await self.db.execute(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == version2,
            )
        )
        v2 = v2_result.scalar_one_or_none()

        if not v1 or not v2:
            raise DocumentNotFoundError("One or both versions not found")

        # Load documents and compare
        doc1 = self.document_handler.load_document(v1.file_path)
        doc2 = self.document_handler.load_document(v2.file_path)

        # Simple text comparison
        text1 = "\n".join(p.text for p in doc1.paragraphs)
        text2 = "\n".join(p.text for p in doc2.paragraphs)

        return {
            "version1": version1,
            "version2": version2,
            "are_identical": text1 == text2,
            "text_length_diff": len(text2) - len(text1),
        }

    async def delete_version(
        self,
        document_id: str,
        version_number: int,
    ) -> dict[str, Any]:
        """Delete a version.

        Args:
            document_id: Document ID.
            version_number: Version to delete.

        Returns:
            Result indicating success.
        """
        from sqlalchemy import delete

        result = await self.db.execute(
            select(DocumentVersion).where(
                DocumentVersion.document_id == document_id,
                DocumentVersion.version_number == version_number,
            )
        )
        version = result.scalar_one_or_none()

        if not version:
            raise DocumentNotFoundError(f"Version {version_number} not found")

        # Delete file
        if version.file_path and os.path.exists(version.file_path):
            os.remove(version.file_path)

        # Delete record
        await self.db.execute(
            delete(DocumentVersion).where(DocumentVersion.id == version.id)
        )
        await self.db.commit()

        return {"success": True, "deleted_version": version_number}
