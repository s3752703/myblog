"""new fields in user model

Revision ID: 0153cfe651c3
Revises: bdfd0d2cbde4
Create Date: 2022-04-12 20:44:48.366144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0153cfe651c3'
down_revision = 'bdfd0d2cbde4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('aboutMe', sa.String(length=200), nullable=True))
    op.add_column('user', sa.Column('lastSeen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'lastSeen')
    op.drop_column('user', 'aboutMe')
    # ### end Alembic commands ###
