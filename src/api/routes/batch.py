"""Batch operation routes.

This module provides endpoints for batch document operations.
"""

import os
import uuid
from typing import Any

from fastapi import APIRouter

from src.core.config import get_settings
from src.core.exceptions import DocumentNotFoundError
from src.handlers.document_handler import DocumentHandler
from src.handlers.text_handler import TextHandler
from src.models.schemas import BatchRequest, BatchResult

router = APIRouter(prefix="/documents/{document_id}/batch")


@router.post(
    "",
    summary="Execute Batch Operations",
    description="Execute multiple operations in a batch.",
)
async def execute_batch(
    document_id: str,
    batch: BatchRequest,
) -> BatchResult:
    """Execute batch operations.

    Args:
        document_id: Document UUID.
        batch: Batch request with operations.

    Returns:
        Batch result with success/failure info.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    doc_handler = DocumentHandler()
    doc_handler.open_document(file_path)
    text_handler = TextHandler(doc_handler.document)

    results: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    success = True

    for i, operation in enumerate(batch.operations):
        try:
            result = execute_operation(
                operation.operation,
                operation.params,
                doc_handler,
                text_handler,
            )
            results.append({
                "index": i,
                "operation": operation.operation,
                "success": True,
                "result": result,
            })
        except Exception as e:
            error = {
                "index": i,
                "operation": operation.operation,
                "error": str(e),
            }
            errors.append(error)
            success = False

            if batch.stop_on_error:
                break

    if success or not batch.stop_on_error:
        doc_handler.save_document()

    return BatchResult(
        success=success,
        results=results,
        errors=errors,
    )


def execute_operation(
    operation: str,
    params: dict[str, Any],
    doc_handler: DocumentHandler,
    text_handler: TextHandler,
) -> dict[str, Any]:
    """Execute a single operation.

    Args:
        operation: Operation name.
        params: Operation parameters.
        doc_handler: Document handler.
        text_handler: Text handler.

    Returns:
        Operation result.
    """
    if operation == "add_paragraph":
        index = text_handler.add_paragraph(
            text=params.get("text", ""),
            style=params.get("style"),
            alignment=params.get("alignment"),
        )
        return {"index": index}

    elif operation == "update_paragraph":
        para = text_handler.update_paragraph(
            index=params["index"],
            text=params.get("text"),
            style=params.get("style"),
        )
        return {"index": para.index}

    elif operation == "delete_paragraph":
        text_handler.delete_paragraph(params["index"])
        return {"deleted": True}

    elif operation == "replace_text":
        count = text_handler.replace_text(
            find=params["find"],
            replace=params["replace"],
            case_sensitive=params.get("case_sensitive", False),
        )
        return {"replaced": count}

    elif operation == "set_metadata":
        doc_handler.set_metadata(
            author=params.get("author"),
            title=params.get("title"),
            subject=params.get("subject"),
            keywords=params.get("keywords"),
            comments=params.get("comments"),
            category=params.get("category"),
        )
        return {"updated": True}

    else:
        raise ValueError(f"Unknown operation: {operation}")


@router.post(
    "/validate",
    summary="Validate Batch",
    description="Validate a batch without executing.",
)
async def validate_batch(
    document_id: str,
    batch: BatchRequest,
) -> dict[str, Any]:
    """Validate batch operations.

    Args:
        document_id: Document UUID.
        batch: Batch request to validate.

    Returns:
        Validation result.
    """
    settings = get_settings()
    file_path = os.path.join(settings.upload_dir, f"{document_id}.docx")

    if not os.path.exists(file_path):
        raise DocumentNotFoundError(document_id)

    valid_operations = [
        "add_paragraph",
        "update_paragraph",
        "delete_paragraph",
        "replace_text",
        "set_metadata",
    ]

    validation_results = []
    all_valid = True

    for i, operation in enumerate(batch.operations):
        is_valid = operation.operation in valid_operations

        if not is_valid:
            all_valid = False

        validation_results.append({
            "index": i,
            "operation": operation.operation,
            "valid": is_valid,
            "error": None if is_valid else f"Unknown operation: {operation.operation}",
        })

    return {
        "valid": all_valid,
        "operation_count": len(batch.operations),
        "results": validation_results,
    }
