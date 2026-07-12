"""add content colum to posts table

Revision ID: e206df6cff0b
Revises: a2f0382056e2
Create Date: 2026-07-12 12:36:42.349586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e206df6cff0b'
down_revision: Union[str, Sequence[str], None] = 'a2f0382056e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
