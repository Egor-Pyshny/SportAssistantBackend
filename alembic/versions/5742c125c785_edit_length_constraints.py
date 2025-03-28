"""edit length constraints

Revision ID: 5742c125c785
Revises: d71754056912
Create Date: 2025-03-23 16:44:38.592244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5742c125c785'
down_revision: Union[str, None] = 'd71754056912'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tbl_coach', 'institution',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.create_unique_constraint(None, 'tbl_comprehensive_examination', ['id'])
    op.create_unique_constraint(None, 'tbl_med_examination', ['id'])
    op.alter_column('tbl_user', 'email',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('tbl_user', 'name',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('tbl_user', 'surname',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('tbl_user', 'sport_type',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('tbl_user', 'qualification',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=255),
               existing_nullable=False)
    op.alter_column('tbl_user', 'address',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('tbl_user', 'sex',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=10),
               existing_nullable=False)
    op.alter_column('tbl_user', 'role',
               existing_type=sa.VARCHAR(length=30),
               type_=sa.String(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tbl_user', 'role',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
    op.alter_column('tbl_user', 'sex',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
    op.alter_column('tbl_user', 'address',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
    op.alter_column('tbl_user', 'qualification',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
    op.alter_column('tbl_user', 'sport_type',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)
    op.alter_column('tbl_user', 'surname',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
    op.alter_column('tbl_user', 'name',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=30),
               existing_nullable=False)
    op.alter_column('tbl_user', 'email',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    op.drop_constraint(None, 'tbl_med_examination', type_='unique')
    op.drop_constraint(None, 'tbl_comprehensive_examination', type_='unique')
    op.alter_column('tbl_coach', 'institution',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)
    # ### end Alembic commands ###
