"""empty message

Revision ID: 7ca9d363ca7f
Revises: 
Create Date: 2019-06-10 20:45:52.085164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ca9d363ca7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('active_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('level', sa.String(length=64), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('apparatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('gymnast',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('surname', sa.String(length=256), nullable=True),
    sa.Column('club', sa.String(length=128), nullable=True),
    sa.Column('age_group', sa.String(length=128), nullable=True),
    sa.Column('level', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'surname', 'club', name='gymnast_ux1')
    )
    op.create_index(op.f('ix_gymnast_level'), 'gymnast', ['level'], unique=False)
    op.create_index(op.f('ix_gymnast_name'), 'gymnast', ['name'], unique=False)
    op.create_table('gymnast_scores',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gymnast_id', sa.Integer(), nullable=True),
    sa.Column('apparatus_id', sa.Integer(), nullable=True),
    sa.Column('final_score', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['apparatus_id'], ['apparatus.id'], ),
    sa.ForeignKeyConstraint(['gymnast_id'], ['gymnast.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('gymnast_scores')
    op.drop_index(op.f('ix_gymnast_name'), table_name='gymnast')
    op.drop_index(op.f('ix_gymnast_level'), table_name='gymnast')
    op.drop_table('gymnast')
    op.drop_table('apparatus')
    op.drop_table('active_set')
    # ### end Alembic commands ###
