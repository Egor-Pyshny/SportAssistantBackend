"""edit user model defaults 2

Revision ID: f54ccaccd8c3
Revises: bab9d65133b1
Create Date: 2025-03-26 17:25:01.460237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f54ccaccd8c3'
down_revision: Union[str, None] = 'bab9d65133b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tbl_user', 'is_info_filled',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tbl_user', 'is_info_filled',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
