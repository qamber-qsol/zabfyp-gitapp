"""add missing hashed_password column

Revision ID: 6b65ad05405c
Revises: 3ab1fe0cabc6
Create Date: 2026-08-03 17:28:32.166634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b65ad05405c'
down_revision: Union[str, None] = '3ab1fe0cabc6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
