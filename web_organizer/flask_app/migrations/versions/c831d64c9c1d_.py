"""empty message

Revision ID: c831d64c9c1d
Revises: 2d4396f06af9
Create Date: 2017-12-03 23:22:28.684786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c831d64c9c1d'
down_revision = '2d4396f06af9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('z_cord', sa.Float(), nullable=True))
    op.drop_column('teams', 'x_cord')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('x_cord', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('teams', 'z_cord')
    # ### end Alembic commands ###