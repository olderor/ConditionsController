"""empty message

Revision ID: edaff1fd2774
Revises: c7023a27bed4
Create Date: 2018-05-21 01:17:19.922245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edaff1fd2774'
down_revision = 'c7023a27bed4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_column('product_types', 'expiration_date_length')
    with op.batch_alter_table('product_types') as batch_op:
        batch_op.drop_column('expiration_date_length')
    op.add_column('user', sa.Column('description', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('image_url', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('name', sa.String(length=120), nullable=True))
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('about_me')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.VARCHAR(length=140), nullable=True))
    op.drop_column('user', 'name')
    op.drop_column('user', 'image_url')
    op.drop_column('user', 'description')
    op.add_column('product_types', sa.Column('expiration_date_length', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###