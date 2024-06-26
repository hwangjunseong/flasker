"""edit crawl

Revision ID: 2f52493325cc
Revises: d4f537b5d95a
Create Date: 2024-05-07 13:36:48.143170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f52493325cc'
down_revision = 'd4f537b5d95a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_index('title')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.create_index('title', ['title'], unique=True)

    # ### end Alembic commands ###
