"""Add achievements

Revision ID: 3746cd036672
Revises: 9ffa7cc683f1
Create Date: 2024-08-16 20:39:49.770967

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3746cd036672'
down_revision: Union[str, None] = '9ffa7cc683f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('achievements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('rate', sa.String(), nullable=True),
    sa.Column('year', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('achievements')
    # ### end Alembic commands ###