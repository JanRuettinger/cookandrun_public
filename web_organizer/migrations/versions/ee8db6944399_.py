"""empty message

Revision ID: ee8db6944399
Revises: 2d16e0c4af70
Create Date: 2017-08-19 23:15:44.648726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee8db6944399'
down_revision = '2d16e0c4af70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('status2', sa.Integer(), nullable=True))
    op.drop_column('events', 'status')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('status', sa.VARCHAR(length=60), autoincrement=False, nullable=True))
    op.drop_column('events', 'status2')
    # ### end Alembic commands ###
