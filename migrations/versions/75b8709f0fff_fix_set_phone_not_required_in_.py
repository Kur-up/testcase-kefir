"""fix: set phone not required in UserAlchemy model

Revision ID: 75b8709f0fff
Revises: 6813bf65c8e1
Create Date: 2023-05-19 11:55:49.445039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75b8709f0fff'
down_revision = '6813bf65c8e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    # ### end Alembic commands ###