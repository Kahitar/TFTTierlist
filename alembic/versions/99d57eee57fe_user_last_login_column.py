"""User last login column

Revision ID: 99d57eee57fe
Revises: 5238b9c8238c
Create Date: 2021-02-02 10:52:53.443191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99d57eee57fe'
down_revision = '5238b9c8238c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', sa.Column('last_login', sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table("User") as batch_op:
        batch_op.drop_column('last_login')
