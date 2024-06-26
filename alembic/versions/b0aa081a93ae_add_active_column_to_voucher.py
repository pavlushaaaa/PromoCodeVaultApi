"""add active column to voucher

Revision ID: b0aa081a93ae
Revises: 62d330e10ac0
Create Date: 2024-05-21 18:40:14.221795

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0aa081a93ae'
down_revision: Union[str, None] = '62d330e10ac0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vouchers', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vouchers', 'active')
    # ### end Alembic commands ###
