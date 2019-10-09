"""empty message

Revision ID: cb306f68dd11
Revises: 01abe9f19892
Create Date: 2019-10-07 07:57:01.936494

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cb306f68dd11'
down_revision = '01abe9f19892'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bots', sa.Column('fitted_state', sa.Integer(), nullable=False))
    op.drop_column('bots', 'enable_flag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bots', sa.Column('enable_flag', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('bots', 'fitted_state')
    # ### end Alembic commands ###