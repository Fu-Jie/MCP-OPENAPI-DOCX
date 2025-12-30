"""Template routes.

This module provides endpoints for template operations.
"""

import os
import uuid
from typing import Any

from fastapi import APIRouter, File, UploadFile

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError, InvalidDocumentError
from src.handlers.document_handler import DocumentHandler
from src.models.schemas import TemplateCreate, TemplateUpdate, TemplateResponse

router = APIRouter(prefix="/templates")

# Simple in-memory template storage (would use database in production)
_templates: dict[str, dict[str, Any]] = {}


@router.get(
    "",
    summary="List Templates",
    description="Get all available templates.",
)
async def list_templates(
    category: str | None = None,
    public_only: bool = False,
) -> dict[str, Any]:
    """List all templates.

    Args:
        category: Optional category filter.
        public_only: Only show public templates.

    Returns:
        List of templates.
    """
    templates = list(_templates.values())

    if category:
        templates = [t for t in templates if t.get("category") == category]

    if public_only:
        templates = [t for t in templates if t.get("is_public", True)]

    return {
        "count": len(templates),
        "templates": templates,
    }


@router.get(
    "/{template_id}",
    summary="Get Template",
    description="Get a template by ID.",
)
async def get_template(template_id: str) -> dict[str, Any]:
    """Get a template.

    Args:
        template_id: Template UUID.

    Returns:
        Template information.
    """
    if template_id not in _templates:
        raise DocumentNotFoundError(template_id, "Template not found")

    return _templates[template_id]


@router.post(
    "",
    summary="Create Template",
    description="Create a new template from a document.",
)
async def create_template(
    data: TemplateCreate,
    file: UploadFile = File(...),
) -> dict[str, Any]:
    """Create a template.

    Args:
        data: Template creation data.
        file: Template file.

    Returns:
        Created template information.
    """
    settings = get_settings()

    # Validate file
    if not file.filename or not file.filename.endswith(".docx"):
        raise InvalidDocumentError("Only .docx files are supported")

    content = await file.read()
    handler = DocumentHandler()
    handler.validate_bytes(content)

    # Save template file
    template_id = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, "templates", f"{template_id}.docx")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(content)

    # Store template metadata
    template = {
        "uuid": template_id,
        "name": data.name,
        "description": data.description,
        "category": data.category,
        "is_public": data.is_public,
        "file_path": file_path,
        "metadata": data.metadata,
    }
    _templates[template_id] = template

    return template


@router.put(
    "/{template_id}",
    summary="Update Template",
    description="Update template metadata.",
)
async def update_template(
    template_id: str,
    data: TemplateUpdate,
) -> dict[str, Any]:
    """Update a template.

    Args:
        template_id: Template UUID.
        data: Update data.

    Returns:
        Updated template information.
    """
    if template_id not in _templates:
        raise DocumentNotFoundError(template_id, "Template not found")

    template = _templates[template_id]

    if data.name is not None:
        template["name"] = data.name
    if data.description is not None:
        template["description"] = data.description
    if data.category is not None:
        template["category"] = data.category
    if data.is_public is not None:
        template["is_public"] = data.is_public

    return template


@router.delete(
    "/{template_id}",
    summary="Delete Template",
    description="Delete a template.",
)
async def delete_template(template_id: str) -> dict[str, Any]:
    """Delete a template.

    Args:
        template_id: Template UUID.

    Returns:
        Deletion confirmation.
    """
    if template_id not in _templates:
        raise DocumentNotFoundError(template_id, "Template not found")

    template = _templates.pop(template_id)

    # Delete file
    if os.path.exists(template["file_path"]):
        os.remove(template["file_path"])

    return {"deleted": True, "template_id": template_id}


@router.post(
    "/{template_id}/create-document",
    summary="Create Document from Template",
    description="Create a new document using a template.",
)
async def create_from_template(
    template_id: str,
    title: str,
) -> dict[str, Any]:
    """Create a document from a template.

    Args:
        template_id: Template UUID.
        title: New document title.

    Returns:
        Created document information.
    """
    settings = get_settings()

    if template_id not in _templates:
        raise DocumentNotFoundError(template_id, "Template not found")

    template = _templates[template_id]

    # Copy template file
    doc_id = str(uuid.uuid4())
    doc_path = os.path.join(settings.upload_dir, f"{doc_id}.docx")

    with open(template["file_path"], "rb") as src:
        with open(doc_path, "wb") as dst:
            dst.write(src.read())

    # Update document metadata
    handler = DocumentHandler()
    handler.open_document(doc_path)
    handler.set_metadata(title=title)
    handler.save_document()

    return {
        "uuid": doc_id,
        "title": title,
        "template_id": template_id,
        "file_path": doc_path,
    }


@router.get(
    "/categories",
    summary="Get Template Categories",
    description="Get all template categories.",
)
async def get_categories() -> dict[str, Any]:
    """Get template categories.

    Returns:
        List of categories.
    """
    categories = set()
    for template in _templates.values():
        if template.get("category"):
            categories.add(template["category"])

    return {
        "categories": list(categories),
    }
