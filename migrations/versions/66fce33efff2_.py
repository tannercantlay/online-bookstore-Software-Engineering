"""empty message

Revision ID: 66fce33efff2
Revises: 984120a385bb
Create Date: 2020-04-08 19:54:28.626416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66fce33efff2'
down_revision = '984120a385bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('card_exp', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('cardtype', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('cardtype')
        batch_op.drop_column('card_exp')

    # ### end Alembic commands ###
