"""empty message

Revision ID: 0a7f81986e5c
Revises: 83d17c7dc4a2
Create Date: 2017-06-03 23:37:33.344861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a7f81986e5c'
down_revision = '83d17c7dc4a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('status', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
