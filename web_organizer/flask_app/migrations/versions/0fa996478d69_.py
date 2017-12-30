"""empty message

Revision ID: 0fa996478d69
Revises: 
Create Date: 2017-12-03 22:01:05.568876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa996478d69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('teams_group_id_fkey', 'teams', type_='foreignkey')
    op.drop_column('teams', 'group_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('teams_group_id_fkey', 'teams', 'groups', ['group_id'], ['id'])
    # ### end Alembic commands ###