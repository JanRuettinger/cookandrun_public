"""change column types in event table

Revision ID: 83d17c7dc4a2
Revises: bf9a77c4b1e1
Create Date: 2017-05-28 19:43:51.278345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83d17c7dc4a2'
down_revision = 'bf9a77c4b1e1'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('events', 'starter_time', existing_type=sa.DateTime(), type_=sa.String())
    op.alter_column('events', 'main_time', existing_type=sa.DateTime(), type_=sa.String())
    op.alter_column('events', 'dessert_time', existing_type=sa.DateTime(), type_=sa.String())


def downgrade():
    op.alter_column('events', 'starter_time', existing_type=sa.String(), type_=sa.DateTime())
    op.alter_column('events', 'main_time', existing_type=sa.String(), type_=sa.DateTime())
    op.alter_column('events', 'dessert_time', existing_type=sa.String(), type_=sa.DateTime())
