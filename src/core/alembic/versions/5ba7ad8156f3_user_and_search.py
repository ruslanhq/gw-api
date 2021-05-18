"""user and search

Revision ID: 5ba7ad8156f3
Revises: 55dcc428fe3b
Create Date: 2021-02-19 15:21:14.501295

"""
from alembic import op
import sqlalchemy as sa
import src.core.fields_sqlalchemy.types


# revision identifiers, used by Alembic.
revision = '5ba7ad8156f3'
down_revision = '55dcc428fe3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('search',
        sa.Column('id', src.core.fields_sqlalchemy.types.uuid.UUIDType(binary=False), nullable=False),
        sa.Column('status', sa.Enum(
            'success', 'running', 'failed',
            name='searchstatus'
        ), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('query', sa.String(length=255), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('dag_id', sa.String(length=255), nullable=True),
        sa.Column('dag_run_id', sa.String(length=255), nullable=True),
        sa.Column('meta_data', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_search_status'), 'search', ['status'], unique=False),
    op.create_index(op.f('ix_search_user_id'), 'search', ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_search_status'), table_name='search')
    op.drop_table('search')
    # ### end Alembic commands ###