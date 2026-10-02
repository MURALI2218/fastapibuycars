"""create tables

Revision ID: 5f113557729a
Revises: 
Create Date: 2026-09-30 18:05:15.016033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f113557729a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cars', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                     sa.Column('model', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('cars')
    pass
