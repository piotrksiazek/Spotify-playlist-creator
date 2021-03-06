"""empty message

Revision ID: edc9a51de04c
Revises: 91245aa1647a
Create Date: 2020-12-30 21:28:07.457381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edc9a51de04c'
down_revision = '91245aa1647a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('spotify_id', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_user_spotify_id'), 'user', ['spotify_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_spotify_id'), table_name='user')
    op.drop_column('user', 'spotify_id')
    # ### end Alembic commands ###
