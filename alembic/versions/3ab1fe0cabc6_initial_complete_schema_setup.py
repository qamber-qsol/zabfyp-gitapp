"""Initial complete schema setup

Revision ID: 3ab1fe0cabc6
Revises: 
Create Date: 2026-07-28 16:30:22.141603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ab1fe0cabc6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
