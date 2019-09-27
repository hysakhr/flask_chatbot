"""empty message

Revision ID: 57594afd54b6
Revises: fbaca439748d
Create Date: 2019-09-27 08:49:12.874724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57594afd54b6'
down_revision = 'fbaca439748d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faqs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.Column('answer', sa.Text(), nullable=False),
    sa.Column('question_org', sa.Text(), nullable=False),
    sa.Column('answer_org', sa.Text(), nullable=False),
    sa.Column('faq_list_id', sa.Integer(), nullable=False),
    sa.Column('enable_flag', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['faq_list_id'], ['faq_lists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('faqs')
    # ### end Alembic commands ###