"""criação inicial das tabelas do banco de dados

Revision ID: 8351bdff29af
Revises: 
Create Date: 2025-07-03 09:19:35.124769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8351bdff29af'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artista',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    op.create_table('musica',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('palavra',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vocabulo', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vocabulo')
    )
    op.create_table('frase',
    sa.Column('id_musica', sa.Integer(), nullable=False),
    sa.Column('indice_frase', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_musica'], ['musica.id'], ),
    sa.PrimaryKeyConstraint('id_musica', 'indice_frase')
    )
    op.create_table('frase_palavra',
    sa.Column('id_musica', sa.Integer(), nullable=False),
    sa.Column('indice_frase', sa.Integer(), nullable=False),
    sa.Column('id_palavra', sa.Integer(), nullable=False),
    sa.Column('indice_palavra', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_musica'], ['musica.id'], ),
    sa.ForeignKeyConstraint(['id_palavra'], ['palavra.id'], ),
    sa.PrimaryKeyConstraint('id_musica', 'indice_frase', 'id_palavra', 'indice_palavra')
    )
    op.create_table('interprete',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_musica', sa.Integer(), nullable=False),
    sa.Column('id_artista', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_artista'], ['artista.id'], ),
    sa.ForeignKeyConstraint(['id_musica'], ['musica.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_musica', 'id_artista', name='idx__musica_artista')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('interprete')
    op.drop_table('frase_palavra')
    op.drop_table('frase')
    op.drop_table('palavra')
    op.drop_table('musica')
    op.drop_table('artista')
    # ### end Alembic commands ###
