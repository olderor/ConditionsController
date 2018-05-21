"""empty message

Revision ID: 36b3ff45f5b8
Revises: 8c9145814fb7
Create Date: 2018-05-21 17:52:24.283902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36b3ff45f5b8'
down_revision = '8c9145814fb7'
branch_labels = None
depends_on = None


def upgrade():
    return
    # ### commands auto generated by Alembic - please adjust! ###
    #op.add_column('tracking_device', sa.Column('password_hash', sa.String(length=120), nullable=True))
    #op.create_index(op.f('ix_tracking_device_key'), 'tracking_device', ['key'], unique=True)
    #op.create_index(op.f('ix_tracking_device_token'), 'tracking_device', ['token'], unique=True)
    #with op.batch_alter_table('tracking_status') as batch_op:
    #    batch_op.drop_column('tracking_device_id')
    #op.create_foreign_key(None, 'tracking_status', 'tracking_device', ['tracking_device_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tracking_status', type_='foreignkey')
    op.create_foreign_key(None, 'tracking_status', 'product', ['date_recordered'], ['id'])
    op.drop_index(op.f('ix_tracking_device_token'), table_name='tracking_device')
    op.drop_index(op.f('ix_tracking_device_key'), table_name='tracking_device')
    op.drop_column('tracking_device', 'password_hash')
    # ### end Alembic commands ###
