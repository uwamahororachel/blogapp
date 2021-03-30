"""third Migration

Revision ID: 6e89beaeaace
Revises: d5f9c0c07716
Create Date: 2021-09-28 18:21:46.253993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e89beaeaace'
down_revision = 'd5f9c0c07716'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'blog_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('comments', 'blog_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
