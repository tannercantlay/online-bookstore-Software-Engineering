"""empty message

Revision ID: fe335683e28f
Revises: 32a5ac7d5cbe
Create Date: 2020-04-07 21:17:20.480789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe335683e28f'
down_revision = '32a5ac7d5cbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'address',
               existing_type=sa.VARCHAR(length=75),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'address',
               existing_type=sa.VARCHAR(length=75),
               nullable=False)
    # ### end Alembic commands ###
