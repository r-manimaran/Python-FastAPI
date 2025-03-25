"""create todos table

Revision ID: b57d143622f0
Revises: 
Create Date: 2025-03-24 10:34:39.225601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b57d143622f0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # op.create_table(
    #     "todos",
    #     sa.Column("id", sa.Integer, primary_key=True),
    #     sa.Column("title", sa.String(100), nullable=False),
    #     sa.Column("description", sa.String(100), nullable=False),
    #     sa.Column("priority", sa.Integer, nullable=False),
    #     sa.Column("complete", sa.Boolean, nullable=False),
    #     sa.Column("created_at", sa.DateTime, nullable=False),
    # )
    op.execute(
        """
        CREATE TABLE todos (
            id BigSERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description VARCHAR(100) NOT NULL,
            priority INTEGER NOT NULL,
            complete BOOLEAN NOT NULL default false,
            created_at TIMESTAMP NOT NULL
        );
        """
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE todos")

