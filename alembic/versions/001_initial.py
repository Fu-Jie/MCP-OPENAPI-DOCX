"""Initial database schema.

Revision ID: 001_initial
Revises: None
Create Date: 2024-01-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial database tables."""

    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("username", sa.String(100), unique=True, nullable=False, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=True),
        sa.Column("is_active", sa.Boolean(), default=True, nullable=False),
        sa.Column("is_superuser", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )

    # Documents table
    op.create_table(
        "documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("current_version", sa.Integer(), default=1, nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("is_locked", sa.Boolean(), default=False, nullable=False),
        sa.Column("locked_by", sa.String(36), nullable=True),
        sa.Column("locked_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_documents_user_id", "documents", ["user_id"])

    # Document versions table
    op.create_table(
        "document_versions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "document_id",
            sa.String(36),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
    )
    op.create_index("ix_document_versions_document_id", "document_versions", ["document_id"])
    op.create_unique_constraint(
        "uq_document_version", "document_versions", ["document_id", "version_number"]
    )

    # Comments table
    op.create_table(
        "comments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "document_id",
            sa.String(36),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("author", sa.String(255), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("paragraph_index", sa.Integer(), nullable=True),
        sa.Column("run_start", sa.Integer(), nullable=True),
        sa.Column("run_end", sa.Integer(), nullable=True),
        sa.Column("parent_id", sa.String(36), sa.ForeignKey("comments.id"), nullable=True),
        sa.Column("is_resolved", sa.Boolean(), default=False, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_comments_document_id", "comments", ["document_id"])

    # Revisions table
    op.create_table(
        "revisions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "document_id",
            sa.String(36),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("author", sa.String(255), nullable=False),
        sa.Column("revision_type", sa.String(50), nullable=False),
        sa.Column("original_text", sa.Text(), nullable=True),
        sa.Column("new_text", sa.Text(), nullable=True),
        sa.Column("paragraph_index", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(50), default="pending", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_revisions_document_id", "revisions", ["document_id"])

    # Templates table
    op.create_table(
        "templates",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(100), nullable=True, index=True),
        sa.Column("tags", sa.JSON(), nullable=True),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    )

    # Audit log table
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), nullable=True, index=True),
        sa.Column("action", sa.String(100), nullable=False, index=True),
        sa.Column("resource_type", sa.String(100), nullable=False),
        sa.Column("resource_id", sa.String(36), nullable=True, index=True),
        sa.Column("details", sa.JSON(), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, index=True),
    )


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table("audit_logs")
    op.drop_table("templates")
    op.drop_table("revisions")
    op.drop_table("comments")
    op.drop_table("document_versions")
    op.drop_table("documents")
    op.drop_table("users")
