"""empty message

Revision ID: 63b64c7bc23b
Revises: 66fce33efff2
Create Date: 2020-04-08 20:30:12.259571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63b64c7bc23b'
down_revision = '66fce33efff2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('card_cvv', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('card_cvv')

    # ### end Alembic commands ###
