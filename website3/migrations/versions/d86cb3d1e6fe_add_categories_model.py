"""Add Categories Model

Revision ID: d86cb3d1e6fe
Revises: 560a2f77c8f4
Create Date: 2024-04-27 21:35:57.141324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd86cb3d1e6fe'
down_revision = '560a2f77c8f4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('categorier_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categorier_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categories')
    # ### end Alembic commands ###
