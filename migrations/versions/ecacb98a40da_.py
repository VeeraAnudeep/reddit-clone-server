"""empty message

Revision ID: ecacb98a40da
Revises: 
Create Date: 2018-03-26 22:32:09.445703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecacb98a40da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('topics', sa.Column('created_on', sa.DateTime(), nullable=False))
    op.alter_column('topics', 'content',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('topics', 'content',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.drop_column('topics', 'created_on')
    # ### end Alembic commands ###