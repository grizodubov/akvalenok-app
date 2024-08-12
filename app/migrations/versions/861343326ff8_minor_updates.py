"""minor updates

Revision ID: 861343326ff8
Revises: ae29c1a2b392
Create Date: 2024-08-10 20:00:33.488253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '861343326ff8'
down_revision: Union[str, None] = 'ae29c1a2b392'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('total_cost', sa.Integer(), sa.Computed('(time_to - time_from) * price', ), nullable=False))
    op.add_column('bookings', sa.Column('total_days', sa.Integer(), sa.Computed('time_to - time_from', ), nullable=False))
    op.alter_column('bookings', 'time_from',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False)
    op.alter_column('bookings', 'time_to',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.Date(),
               existing_nullable=False)
    op.add_column('users', sa.Column('role', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'role')
    op.alter_column('bookings', 'time_to',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.alter_column('bookings', 'time_from',
               existing_type=sa.Date(),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=False)
    op.drop_column('bookings', 'total_days')
    op.drop_column('bookings', 'total_cost')
    # ### end Alembic commands ###
