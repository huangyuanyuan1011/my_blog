"""empty message

Revision ID: 411b9174fa2c
Revises: 793b7bf05840
Create Date: 2018-01-02 21:25:49.557711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '411b9174fa2c'
down_revision = '793b7bf05840'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rid', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_rid'), 'posts', ['rid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_rid'), table_name='posts')
    op.drop_table('posts')
    # ### end Alembic commands ###
