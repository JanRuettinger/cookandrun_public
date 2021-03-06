"""empty message

Revision ID: 4b55e5cd53f0
Revises: 5a673b0db2f2
Create Date: 2017-12-04 22:41:24.814078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b55e5cd53f0'
down_revision = '5a673b0db2f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('teams_host_1_id_fkey', 'teams', type_='foreignkey')
    op.drop_constraint('teams_host_2_id_fkey', 'teams', type_='foreignkey')
    op.drop_constraint('teams_host_3_id_fkey', 'teams', type_='foreignkey')
    op.create_foreign_key(None, 'teams', 'teams', ['host_1_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'teams', 'teams', ['host_3_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'teams', 'teams', ['host_2_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'teams', type_='foreignkey')
    op.drop_constraint(None, 'teams', type_='foreignkey')
    op.drop_constraint(None, 'teams', type_='foreignkey')
    op.create_foreign_key('teams_host_3_id_fkey', 'teams', 'teams', ['host_3_id'], ['id'])
    op.create_foreign_key('teams_host_2_id_fkey', 'teams', 'teams', ['host_2_id'], ['id'])
    op.create_foreign_key('teams_host_1_id_fkey', 'teams', 'teams', ['host_1_id'], ['id'])
    # ### end Alembic commands ###
