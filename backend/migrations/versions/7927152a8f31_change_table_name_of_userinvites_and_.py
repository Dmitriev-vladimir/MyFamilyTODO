"""Change table name of userInvites and add field result

Revision ID: 7927152a8f31
Revises: 1f8a3dadd080
Create Date: 2023-12-03 19:48:30.286873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7927152a8f31'
down_revision: Union[str, None] = '1f8a3dadd080'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_invite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_sender_id', sa.Integer(), nullable=False),
    sa.Column('user_inviter_id', sa.Integer(), nullable=False),
    sa.Column('target_workspace_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('result', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['target_workspace_id'], ['workspace.id'], ),
    sa.ForeignKeyConstraint(['user_inviter_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_sender_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_invites')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_invites',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_sender_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_inviter_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('target_workspace_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['target_workspace_id'], ['workspace.id'], name='user_invites_target_workspace_id_fkey'),
    sa.ForeignKeyConstraint(['user_inviter_id'], ['user.id'], name='user_invites_user_inviter_id_fkey'),
    sa.ForeignKeyConstraint(['user_sender_id'], ['user.id'], name='user_invites_user_sender_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_invites_pkey')
    )
    op.drop_table('user_invite')
    # ### end Alembic commands ###
