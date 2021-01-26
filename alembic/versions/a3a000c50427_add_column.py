"""Add Column

Revision ID: a3a000c50427
Revises:
Create Date: 2021-01-25 10:45:35.033277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3a000c50427'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Post', sa.Column(
        'image_file', sa.String(20), nullable=True))


def downgrade():
    with op.batch_alter_table("Post") as batch_op:
        batch_op.drop_column('image_file')
