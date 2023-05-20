"""fix: set some columns nullable for UserAlchemy model

Revision ID: 4bd510b82d96
Revises: 9a77b3996d37
Create Date: 2023-05-17 17:37:06.761632

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bd510b82d96'
down_revision = '9a77b3996d37'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'other_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    op.alter_column('users', 'additional_info',
               existing_type=sa.VARCHAR(length=512),
               nullable=True)
    op.alter_column('users', 'temp_token',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'temp_token',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('users', 'additional_info',
               existing_type=sa.VARCHAR(length=512),
               nullable=False)
    op.alter_column('users', 'other_name',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###
