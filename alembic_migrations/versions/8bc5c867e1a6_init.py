"""init

Revision ID: 8bc5c867e1a6
Revises: 
Create Date: 2024-08-06 12:29:20.859441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc5c867e1a6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session',
    sa.Column('session_id', sa.String(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('video',
    sa.Column('video_id', sa.Integer(), nullable=False),
    sa.Column('external_video_id', sa.String(), nullable=False),
    sa.Column('session_id', sa.String(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['session_id'], ['session.session_id'], ),
    sa.PrimaryKeyConstraint('video_id'),
    sa.UniqueConstraint('external_video_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    op.drop_table('session')
    # ### end Alembic commands ###
