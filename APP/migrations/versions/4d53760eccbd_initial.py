"""initial

Revision ID: 4d53760eccbd
Revises: 
Create Date: 2021-04-12 03:12:58.519302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d53760eccbd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('verified_email', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('picture', sa.String(length=100), nullable=False),
    sa.Column('locale', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coach',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position', sa.String(length=100), nullable=False),
    sa.Column('organization', sa.String(length=100), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('linkedin', sa.String(length=100), nullable=False),
    sa.Column('twitter', sa.String(length=50), nullable=False),
    sa.Column('shortdescription', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('coach')
    op.drop_table('users')
    # ### end Alembic commands ###