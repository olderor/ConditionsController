"""empty message

Revision ID: 86087e1ad0b0
Revises: 
Create Date: 2018-05-20 20:04:44.022175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86087e1ad0b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('about', sa.String(length=120), nullable=True),
    sa.Column('image_url', sa.String(length=120), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tracking_device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=120), nullable=True),
    sa.Column('token', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('expiration_date_length', sa.DateTime(), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('image_url', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('role', sa.String(length=30), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_table('condition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('min_value', sa.Integer(), nullable=True),
    sa.Column('max_value', sa.Integer(), nullable=True),
    sa.Column('product_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('tracking_device_id', sa.Integer(), nullable=True),
    sa.Column('product_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['product_type_id'], ['product_types.id'], ),
    sa.ForeignKeyConstraint(['tracking_device_id'], ['tracking_device.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('storing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tracking_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('condition_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('date_recordered', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['condition_id'], ['condition.id'], ),
    sa.ForeignKeyConstraint(['date_recordered'], ['product.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tracking_status')
    op.drop_table('storing')
    op.drop_table('product')
    op.drop_table('condition')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('product_types')
    op.drop_table('tracking_device')
    op.drop_table('organization')
    # ### end Alembic commands ###
