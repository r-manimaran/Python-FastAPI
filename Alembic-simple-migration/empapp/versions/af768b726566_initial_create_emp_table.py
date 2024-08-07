"""Initial_Create_emp_table

Revision ID: af768b726566
Revises: 
Create Date: 2024-07-13 10:17:48.441320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af768b726566'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
    sa.Column('id', sa.BIGINT(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('email', sa.VARCHAR(length=30), nullable=False),
    sa.Column('created_by', sa.String(length=50), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')
    # ### end Alembic commands ###
