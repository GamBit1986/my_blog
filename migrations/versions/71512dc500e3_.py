"""empty message

Revision ID: 71512dc500e3
Revises: c53707bfcb7d
Create Date: 2023-04-08 14:48:41.850472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71512dc500e3'
down_revision = 'c53707bfcb7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('is_staff', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_staff')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
