"""empty message

Revision ID: 5c36b0f5c833
Revises: 3629d0c90e24
Create Date: 2019-10-19 01:51:56.376227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c36b0f5c833'
down_revision = '3629d0c90e24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('domain', sa.Text(), nullable=False),
    sa.Column('enable_flag', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('site_url_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url_pattern', sa.Text(), nullable=False),
    sa.Column('site_id', sa.Integer(), nullable=False),
    sa.Column('bot_id', sa.Integer(), nullable=True),
    sa.Column('enable_flag', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['bot_id'], ['bots.id'], ),
    sa.ForeignKeyConstraint(['site_id'], ['sites.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('site_static_answer_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('site_url_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.Text(), nullable=False),
    sa.Column('static_answer_id', sa.Integer(), nullable=False),
    sa.Column('enable_flag', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['site_url_id'], ['site_url_settings.id'], ),
    sa.ForeignKeyConstraint(['static_answer_id'], ['static_answers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('site_static_answer_settings')
    op.drop_table('site_url_settings')
    op.drop_table('sites')
    # ### end Alembic commands ###