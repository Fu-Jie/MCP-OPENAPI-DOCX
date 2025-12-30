"""Template service for template management.

This module provides the TemplateService class for managing
document templates.
"""

import os
import shutil
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.exceptions import DocumentProcessingError, TemplateNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.models.database import Template


class TemplateService:
    """Service class for template operations.

    Attributes:
        db: Database session.
        document_handler: Handler for document operations.
        settings: Application settings.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the template service.

        Args:
            db: Async database session.
        """
        self.db = db
        self.document_handler = DocumentHandler()
        self.settings = get_settings()

    async def create_template(
        self,
        name: str,
        content: bytes,
        description: str | None = None,
        category: str | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
    ) -> dict[str, Any]:
        """Create a new template.

        Args:
            name: Template name.
            content: Template file content.
            description: Optional description.
            category: Optional category.
            tags: Optional tags.
            user_id: Optional creator ID.

        Returns:
            Created template details.
        """
        try:
            template_id = str(uuid.uuid4())
            templates_dir = os.path.join(self.settings.upload_dir, "templates")
            os.makedirs(templates_dir, exist_ok=True)
            file_path = os.path.join(templates_dir, f"{template_id}.docx")

            with open(file_path, "wb") as f:
                f.write(content)

            template = Template(
                id=template_id,
                name=name,
                file_path=file_path,
                description=description,
                category=category,
                tags=tags or [],
                created_by=user_id,
                created_at=datetime.utcnow(),
            )

            self.db.add(template)
            await self.db.commit()

            return {
                "id": template_id,
                "name": name,
                "description": description,
                "category": category,
                "tags": tags,
            }
        except Exception as e:
            await self.db.rollback()
            raise DocumentProcessingError(f"Failed to create template: {str(e)}")

    async def get_template(self, template_id: str) -> dict[str, Any]:
        """Get template by ID.

        Args:
            template_id: Template ID.

        Returns:
            Template details.

        Raises:
            TemplateNotFoundError: If template not found.
        """
        result = await self.db.execute(
            select(Template).where(Template.id == template_id)
        )
        template = result.scalar_one_or_none()

        if not template:
            raise TemplateNotFoundError(f"Template {template_id} not found")

        return {
            "id": template.id,
            "name": template.name,
            "description": template.description,
            "category": template.category,
            "tags": template.tags,
            "created_at": (
                template.created_at.isoformat() if template.created_at else None
            ),
        }

    async def list_templates(
        self,
        category: str | None = None,
        search: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        """List templates with pagination.

        Args:
            category: Optional category filter.
            search: Optional search query.
            skip: Records to skip.
            limit: Maximum records.

        Returns:
            Tuple of (templates list, total count).
        """
        query = select(Template)

        if category:
            query = query.where(Template.category == category)
        if search:
            query = query.where(Template.name.ilike(f"%{search}%"))

        # Count
        count_result = await self.db.execute(query)
        total = len(count_result.all())

        # Paginate
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        templates = result.scalars().all()

        return [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "category": t.category,
            }
            for t in templates
        ], total

    async def delete_template(self, template_id: str) -> dict[str, Any]:
        """Delete a template.

        Args:
            template_id: Template ID.

        Returns:
            Result indicating success.
        """
        result = await self.db.execute(
            select(Template).where(Template.id == template_id)
        )
        template = result.scalar_one_or_none()

        if not template:
            raise TemplateNotFoundError(f"Template {template_id} not found")

        if template.file_path and os.path.exists(template.file_path):
            os.remove(template.file_path)

        await self.db.execute(delete(Template).where(Template.id == template_id))
        await self.db.commit()

        return {"success": True, "deleted": template_id}

    async def create_document_from_template(
        self,
        template_id: str,
        document_name: str,
        user_id: str,
    ) -> dict[str, Any]:
        """Create a document from template.

        Args:
            template_id: Template ID.
            document_name: Name for new document.
            user_id: User ID.

        Returns:
            Created document details.
        """
        result = await self.db.execute(
            select(Template).where(Template.id == template_id)
        )
        template = result.scalar_one_or_none()

        if not template:
            raise TemplateNotFoundError(f"Template {template_id} not found")

        doc_id = str(uuid.uuid4())
        dest_path = os.path.join(self.settings.upload_dir, f"{doc_id}.docx")

        shutil.copy2(template.file_path, dest_path)

        return {
            "document_id": doc_id,
            "name": document_name,
            "template_id": template_id,
            "file_path": dest_path,
        }

    async def get_categories(self) -> list[str]:
        """Get all template categories.

        Returns:
            List of categories.
        """
        result = await self.db.execute(
            select(Template.category).distinct().where(Template.category.isnot(None))
        )
        return [row[0] for row in result.all()]
