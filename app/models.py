from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, ForeignKeyConstraint

from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Tabela de artistas
class Artista(Base):
    __tablename__ = "artista"
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    interpretes = relationship("Interprete", back_populates="artista", cascade="all, delete")

# Tabela de músicas
class Musica(Base):
    __tablename__ = "musica"
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    interpretes = relationship("Interprete", back_populates="musica", cascade="all, delete")
    frases = relationship("Frase", back_populates="musica", cascade="all, delete")

# Associação entre músicas e artistas
class Interprete(Base):
    __tablename__ = "interprete"
    id = Column(Integer, primary_key=True)
    id_musica = Column(Integer, ForeignKey("musica.id"), nullable=False)
    id_artista = Column(Integer, ForeignKey("artista.id"), nullable=False)
    musica = relationship("Musica", back_populates="interpretes")
    artista = relationship("Artista", back_populates="interpretes")
    __table_args__ = (UniqueConstraint("id_musica", "id_artista", name="idx__musica_artista"),)

# Frases da música
class Frase(Base):
    __tablename__ = "frase"
    # Chave primária composta
    id_musica = Column(Integer, ForeignKey("musica.id"), primary_key=True)
    indice_frase = Column(Integer, primary_key=True)

    musica = relationship("Musica", back_populates="frases")
    # Aqui o relationship vai inferir a join condition a partir da ForeignKeyConstraint em FrasePalavra
    palavras_frase = relationship("FrasePalavra", back_populates="frase", cascade="all, delete")


# Palavras
class Palavra(Base):
    __tablename__ = "palavra"
    id = Column(Integer, primary_key=True)
    vocabulo = Column(String, unique=True, nullable=False)


# Associação entre frase e palavras
class FrasePalavra(Base):
    __tablename__ = "frase_palavra"
    id_musica = Column(Integer, primary_key=True)
    indice_frase = Column(Integer, primary_key=True)
    id_palavra = Column(Integer, ForeignKey("palavra.id"), primary_key=True)
    indice_palavra = Column(Integer, primary_key=True)

    # *** CORREÇÃO AQUI: Adicionar ForeignKeyConstraint explícito para a chave composta da Frase ***
    __table_args__ = (
        ForeignKeyConstraint(
            ['id_musica', 'indice_frase'],
            ['frase.id_musica', 'frase.indice_frase']
        ),
        # Se você quiser que a combinação completa (musica, frase_idx, palavra, palavra_idx)
        # seja única, mantenha o PrimaryKeyConstraint nas colunas.
        # Ou, se for apenas uma chave composta para o FK e o id for uma PK separada,
        # você pode adicionar um 'id' autoincrementável e usar um UniqueConstraint.
        # Por enquanto, mantemos suas PKs existentes para o exemplo.
        # UniqueConstraint('id_musica', 'indice_frase', 'id_palavra', 'indice_palavra', name='idx_frase_palavra_unique')
    )

    # Definir o relationship explícitamente para a chave composta
    frase = relationship(
        "Frase",
        primaryjoin="and_("
                    "FrasePalavra.id_musica == Frase.id_musica,"
                    "FrasePalavra.indice_frase == Frase.indice_frase"
                    ")",
        back_populates="palavras_frase"
    )
    palavra = relationship("Palavra")

