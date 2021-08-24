"""empty message

Revision ID: 19391256a012
Revises: 649e20345a5b
Create Date: 2021-08-24 07:00:01.927381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19391256a012'
down_revision = '649e20345a5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('movies', sa.ARRAY(sa.Integer()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'movies')
    # ### end Alembic commands ###
