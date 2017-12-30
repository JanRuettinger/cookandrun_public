"""empty message

Revision ID: d96e326a357c
Revises: 7969016dbc50
Create Date: 2017-08-19 16:36:09.253181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd96e326a357c'
down_revision = '7969016dbc50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('dessert_1_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_1_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_1_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_2_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_2_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_2_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_3_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_3_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('dessert_3_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_1_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_1_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_1_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_2_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_2_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_2_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_3_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_3_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('main_3_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_1_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_1_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_1_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_2_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_2_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_2_host', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_3_guest_1', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_3_guest_2', sa.Integer(), nullable=True))
    op.add_column('groups', sa.Column('starter_3_host', sa.Integer(), nullable=True))
    op.drop_constraint('groups_main_1_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_main_3_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_starter_1_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_starter_3_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_main_2_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_dessert_3_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_starter_2_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_dessert_1_id_fkey', 'groups', type_='foreignkey')
    op.drop_constraint('groups_dessert_2_id_fkey', 'groups', type_='foreignkey')
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_3_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_1_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_1_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_2_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_2_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_2_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_1_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_2_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_3_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_2_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_3_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_1_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_3_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_2_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_1_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_2_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_3_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_3_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_2_guest_1'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_1_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_1_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['starter_3_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_3_host'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_2_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_1_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['main_3_guest_2'], ['id'])
    op.create_foreign_key(None, 'groups', 'teams', ['dessert_1_guest_1'], ['id'])
    op.drop_column('groups', 'starter_1_id')
    op.drop_column('groups', 'dessert_1_id')
    op.drop_column('groups', 'starter_3_id')
    op.drop_column('groups', 'dessert_3_id')
    op.drop_column('groups', 'main_2_id')
    op.drop_column('groups', 'main_3_id')
    op.drop_column('groups', 'dessert_2_id')
    op.drop_column('groups', 'starter_2_id')
    op.drop_column('groups', 'main_1_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('main_1_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('starter_2_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('dessert_2_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('main_3_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('main_2_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('dessert_3_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('starter_3_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('dessert_1_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('groups', sa.Column('starter_1_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.drop_constraint(None, 'groups', type_='foreignkey')
    op.create_foreign_key('groups_dessert_2_id_fkey', 'groups', 'teams', ['dessert_2_id'], ['id'])
    op.create_foreign_key('groups_dessert_1_id_fkey', 'groups', 'teams', ['dessert_1_id'], ['id'])
    op.create_foreign_key('groups_starter_2_id_fkey', 'groups', 'teams', ['starter_2_id'], ['id'])
    op.create_foreign_key('groups_dessert_3_id_fkey', 'groups', 'teams', ['dessert_3_id'], ['id'])
    op.create_foreign_key('groups_main_2_id_fkey', 'groups', 'teams', ['main_2_id'], ['id'])
    op.create_foreign_key('groups_starter_3_id_fkey', 'groups', 'teams', ['starter_3_id'], ['id'])
    op.create_foreign_key('groups_starter_1_id_fkey', 'groups', 'teams', ['starter_1_id'], ['id'])
    op.create_foreign_key('groups_main_3_id_fkey', 'groups', 'teams', ['main_3_id'], ['id'])
    op.create_foreign_key('groups_main_1_id_fkey', 'groups', 'teams', ['main_1_id'], ['id'])
    op.drop_column('groups', 'starter_3_host')
    op.drop_column('groups', 'starter_3_guest_2')
    op.drop_column('groups', 'starter_3_guest_1')
    op.drop_column('groups', 'starter_2_host')
    op.drop_column('groups', 'starter_2_guest_2')
    op.drop_column('groups', 'starter_2_guest_1')
    op.drop_column('groups', 'starter_1_host')
    op.drop_column('groups', 'starter_1_guest_2')
    op.drop_column('groups', 'starter_1_guest_1')
    op.drop_column('groups', 'main_3_host')
    op.drop_column('groups', 'main_3_guest_2')
    op.drop_column('groups', 'main_3_guest_1')
    op.drop_column('groups', 'main_2_host')
    op.drop_column('groups', 'main_2_guest_2')
    op.drop_column('groups', 'main_2_guest_1')
    op.drop_column('groups', 'main_1_host')
    op.drop_column('groups', 'main_1_guest_2')
    op.drop_column('groups', 'main_1_guest_1')
    op.drop_column('groups', 'dessert_3_host')
    op.drop_column('groups', 'dessert_3_guest_2')
    op.drop_column('groups', 'dessert_3_guest_1')
    op.drop_column('groups', 'dessert_2_host')
    op.drop_column('groups', 'dessert_2_guest_2')
    op.drop_column('groups', 'dessert_2_guest_1')
    op.drop_column('groups', 'dessert_1_host')
    op.drop_column('groups', 'dessert_1_guest_2')
    op.drop_column('groups', 'dessert_1_guest_1')
    # ### end Alembic commands ###
