"""Initial migration

Revision ID: 0457637600c5
Revises: 
Create Date: 2024-08-13 12:50:02.430269

"""
from typing import Sequence, Union

import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0457637600c5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('spaces',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('services', sa.JSON(), nullable=True),
    sa.Column('pools_quantity', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('phone_number', sqlalchemy_utils.types.phone_number.PhoneNumberType(length=20), nullable=True),
    sa.Column('is_problem_client', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('pools',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('space_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('services', sa.JSON(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['space_id'], ['spaces.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('pool_id', sa.Integer(), nullable=False),
    sa.Column('time_from', sa.DateTime(), nullable=False),
    sa.Column('time_to', sa.DateTime(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('total_cost', sa.Integer(), sa.Computed('(EXTRACT(EPOCH FROM (time_to - time_from)) / 1800) * price', ), nullable=False),
    sa.Column('total_half_hours', sa.Integer(), sa.Computed('(EXTRACT(EPOCH FROM (time_to - time_from)) / 1800)', ), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['pool_id'], ['pools.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bookings')
    op.drop_table('pools')
    op.drop_table('users')
    op.drop_table('spaces')
    # ### end Alembic commands ###