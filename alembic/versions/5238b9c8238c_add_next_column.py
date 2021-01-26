"""Add next column

Revision ID: 5238b9c8238c
Revises: a3a000c50427
Create Date: 2021-01-26 11:52:01.748369

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5238b9c8238c'
down_revision = 'a3a000c50427'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Tierlist', sa.Column('name', sa.String(
        100), nullable=False, server_default="New Tierlist"))

    op.add_column('Tierlist', sa.Column(
        'is_public', sa.Integer))


def downgrade():
    with op.batch_alter_table("Tierlist") as batch_op:
        batch_op.drop_column('name')
        batch_op.drop_column('is_public')
