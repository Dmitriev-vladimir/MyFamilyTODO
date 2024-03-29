"""Add workspace relation into Task, Tag and Color

Revision ID: 0503ef881335
Revises: 3ff6bd07779f
Create Date: 2024-01-08 09:43:47.281386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0503ef881335'
down_revision: Union[str, None] = '3ff6bd07779f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('color', sa.Column('workspace_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'color', 'workspace', ['workspace_id'], ['id'])
    op.add_column('tag', sa.Column('workspace_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tag', 'workspace', ['workspace_id'], ['id'])
    op.add_column('task', sa.Column('workspace_id', sa.Integer(), nullable=True))
    op.alter_column('task', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'task', 'workspace', ['workspace_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.alter_column('task', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('task', 'workspace_id')
    op.drop_constraint(None, 'tag', type_='foreignkey')
    op.drop_column('tag', 'workspace_id')
    op.drop_constraint(None, 'color', type_='foreignkey')
    op.drop_column('color', 'workspace_id')
    # ### end Alembic commands ###
