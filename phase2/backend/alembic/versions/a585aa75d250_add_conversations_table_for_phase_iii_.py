"""Add conversations table for Phase III chatbot

Revision ID: a585aa75d250
Revises: 9fe3eaf6b1ee
Create Date: 2026-01-13 02:34:54.130949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a585aa75d250'
down_revision: Union[str, Sequence[str], None] = '9fe3eaf6b1ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add conversations table."""
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True, server_default='New Conversation'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_user_conversations', 'user_id', 'updated_at')
    )


def downgrade() -> None:
    """Downgrade schema - Remove conversations table."""
    op.drop_index('idx_user_conversations', table_name='conversations')
    op.drop_table('conversations')
