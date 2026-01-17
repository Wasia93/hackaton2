"""Add messages table for Phase III chatbot

Revision ID: 7e18eb43eb3f
Revises: a585aa75d250
Create Date: 2026-01-13 02:35:31.311087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e18eb43eb3f'
down_revision: Union[str, Sequence[str], None] = 'a585aa75d250'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - Add messages table."""
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_conversation_messages', 'conversation_id', 'created_at')
    )


def downgrade() -> None:
    """Downgrade schema - Remove messages table."""
    op.drop_index('idx_conversation_messages', table_name='messages')
    op.drop_table('messages')
