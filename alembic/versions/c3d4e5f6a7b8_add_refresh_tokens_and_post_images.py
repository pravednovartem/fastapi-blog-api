"""Add refresh tokens and post images.

Revision ID: c3d4e5f6a7b8
Revises: b1c2a3d4e5f6
Create Date: 2026-06-12 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str], None] = "b1c2a3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "auth_refresh_token",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["auth_user.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index(
        op.f("ix_auth_refresh_token_id"),
        "auth_refresh_token",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_auth_refresh_token_user_id"),
        "auth_refresh_token",
        ["user_id"],
        unique=False,
    )

    op.create_table(
        "blog_post_image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["blog_post.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_blog_post_image_id"),
        "blog_post_image",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_blog_post_image_post_id"),
        "blog_post_image",
        ["post_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_blog_post_image_post_id"),
        table_name="blog_post_image",
    )
    op.drop_index(op.f("ix_blog_post_image_id"), table_name="blog_post_image")
    op.drop_table("blog_post_image")

    op.drop_index(
        op.f("ix_auth_refresh_token_user_id"),
        table_name="auth_refresh_token",
    )
    op.drop_index(
        op.f("ix_auth_refresh_token_id"),
        table_name="auth_refresh_token",
    )
    op.drop_table("auth_refresh_token")
