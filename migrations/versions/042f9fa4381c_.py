"""empty message

Revision ID: 042f9fa4381c
Revises: b3992d394ca2
Create Date: 2019-10-15 10:12:56.397679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '042f9fa4381c'
down_revision = 'b3992d394ca2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('faq_lists', sa.Column('bot_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'faq_lists', 'bots', ['bot_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'faq_lists', type_='foreignkey')
    op.drop_column('faq_lists', 'bot_id')
    # ### end Alembic commands ###