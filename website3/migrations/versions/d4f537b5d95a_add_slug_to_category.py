"""Add slug to category

Revision ID: d4f537b5d95a
Revises: c9681525dddb
Create Date: 2024-05-03 20:02:46.950487

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd4f537b5d95a'
down_revision = 'c9681525dddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=255), nullable=True))
        batch_op.drop_column('slug')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_column('category')

    # ### end Alembic commands ###
