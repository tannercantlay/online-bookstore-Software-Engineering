"""empty message

Revision ID: 8757f29f00bb
Revises: f0ece690bc5e
Create Date: 2020-04-22 15:38:40.347457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8757f29f00bb'
down_revision = 'f0ece690bc5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###