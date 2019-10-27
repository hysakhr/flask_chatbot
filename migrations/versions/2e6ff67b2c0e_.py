"""empty message

Revision ID: 2e6ff67b2c0e
Revises: 
Create Date: 2019-10-27 10:57:30.157731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e6ff67b2c0e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('enable_flag', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('faq_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('bot_id', sa.Integer(), nullable=False),
    sa.Column('start_faq_id', sa.Integer(), nullable=True),
    sa.Column('not_found_faq_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('fitted_model_path', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('fitted_faq_list_id', sa.Integer(), nullable=True),
    sa.Column('fitted_state', sa.Integer(), nullable=False),
    sa.Column('last_fitted_at', sa.DateTime(), nullable=True),
    sa.Column('enable_flag', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['fitted_faq_list_id'], ['faq_lists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
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

    op.create_foreign_key('faq_lists_bot_id', 'faq_lists', 'bots', ['bot_id'], ['id'])
    op.create_foreign_key('faq_lists_not_found_faq_id', 'faq_lists', 'faqs', ['not_found_faq_id'], ['id'])
    op.create_foreign_key('faq_lists_start_faq_id', 'faq_lists', 'faqs', ['start_faq_id'], ['id'])

    op.create_table('faqs_faqs',
    sa.Column('faq_id', sa.Integer(), nullable=False),
    sa.Column('faq_list_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['faq_id'], ['faqs.id'], ),
    sa.ForeignKeyConstraint(['faq_list_id'], ['faq_lists.id'], )
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
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_table('site_url_settings')
    op.drop_table('faqs_faqs')
    op.drop_constraint('faq_lists_start_faq_id', 'faq_lists', type_='foreignkey')
    op.drop_constraint('faq_lists_not_found_faq_id', 'faq_lists', type_='foreignkey')
    op.drop_constraint('faq_lists_bot_id', 'faq_lists', type_='foreignkey')
    op.drop_table('faqs')
    op.drop_table('bots')
    op.drop_table('faq_lists')
    op.drop_table('sites')
    # ### end Alembic commands ###
