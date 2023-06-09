"""fix: set city not required in UserAlchemy model

Revision ID: bc5e371dee4e
Revises: 75b8709f0fff
Create Date: 2023-05-19 11:57:39.333131

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc5e371dee4e'
down_revision = '75b8709f0fff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'city',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'city',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
