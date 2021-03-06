"""empty message

Revision ID: 5b48190171de
Revises: edaff1fd2774
Create Date: 2018-05-21 11:23:02.788226

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b48190171de'
down_revision = 'edaff1fd2774'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('condition', sa.Column('description', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('condition', 'description')
    # ### end Alembic commands ###
