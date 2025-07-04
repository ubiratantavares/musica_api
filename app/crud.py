from sqlalchemy.orm import Session
from . import models, schemas

# ===================== MÚSICA =====================
def criar_musica(db: Session, musica: schemas.MusicaCreate):
    db_musica = models.Musica(titulo=musica.titulo)
    db.add(db_musica)
    db.commit()
    db.refresh(db_musica)
    return db_musica

def listar_musicas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Musica).offset(skip).limit(limit).all()

def buscar_musica_por_id(db: Session, musica_id: int):
    return db.query(models.Musica).filter_by(id=musica_id).first()

def buscar_musica_por_titulo(db: Session, titulo: str):
    return db.query(models.Musica).filter_by(titulo=titulo).first()

def deletar_musica(db: Session, musica_id: int):
    musica = buscar_musica_por_id(db, musica_id)
    if musica:
        db.delete(musica)
        db.commit()
    return musica


# ===================== ARTISTA =====================
def criar_artista(db: Session, artista: schemas.ArtistaCreate):
    db_artista = models.Artista(nome=artista.nome)
    db.add(db_artista)
    db.commit()
    db.refresh(db_artista)
    return db_artista

def listar_artistas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artista).offset(skip).limit(limit).all()

def buscar_artista_por_id(db: Session, artista_id: int):
    return db.query(models.Artista).filter_by(id=artista_id).first()

def buscar_artista_por_nome(db: Session, nome: str):
    return db.query(models.Artista).filter_by(nome=nome).first()

def deletar_artista(db: Session, artista_id: int):
    artista = buscar_artista_por_id(db, artista_id)
    if artista:
        db.delete(artista)
        db.commit()
    return artista


# ===================== PALAVRA =====================
def criar_palavra(db: Session, palavra: schemas.PalavraCreate):
    palavra_existente = buscar_palavra_por_vocabulo(db, palavra.vocabulo)
    if palavra_existente:
        return palavra_existente
    db_palavra = models.Palavra(vocabulo=palavra.vocabulo)
    db.add(db_palavra)
    db.commit()
    db.refresh(db_palavra)
    return db_palavra

def listar_palavras(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Palavra).offset(skip).limit(limit).all()

def buscar_palavra_por_id(db: Session, palavra_id: int):
    return db.query(models.Palavra).filter_by(id=palavra_id).first()

def buscar_palavra_por_vocabulo(db: Session, vocabulo: str):
    return db.query(models.Palavra).filter_by(vocabulo=vocabulo).first()

def deletar_palavra(db: Session, palavra_id: int):
    palavra = buscar_palavra_por_id(db, palavra_id)
    if palavra:
        db.delete(palavra)
        db.commit()
    return palavra


# ===================== INTERPRETE =====================
def criar_interprete(db: Session, interprete: schemas.InterpreteCreate):
    existente = buscar_interprete_por_musica_artista(db, interprete.id_musica, interprete.id_artista)
    if existente:
        return existente
    db_interprete = models.Interprete(
        id_musica=interprete.id_musica,
        id_artista=interprete.id_artista
    )
    db.add(db_interprete)
    db.commit()
    db.refresh(db_interprete)
    return db_interprete

def listar_interpretes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Interprete).offset(skip).limit(limit).all()

def buscar_interprete_por_id(db: Session, interprete_id: int):
    return db.query(models.Interprete).filter_by(id=interprete_id).first()

def buscar_interprete_por_musica_artista(db: Session, musica_id: int, artista_id: int):
    return db.query(models.Interprete).filter_by(id_musica=musica_id, id_artista=artista_id).first()

def deletar_interprete(db: Session, interprete_id: int):
    interprete = buscar_interprete_por_id(db, interprete_id)
    if interprete:
        db.delete(interprete)
        db.commit()
    return interprete


# ===================== FRASE =====================
def criar_frase(db: Session, frase: schemas.FraseCreate):
    db_frase = models.Frase(
        id_musica=frase.id_musica,
        indice_frase=frase.indice_frase
    )
    db.add(db_frase)
    db.commit()
    db.refresh(db_frase)
    return db_frase

def listar_frases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Frase).offset(skip).limit(limit).all()

def buscar_frase(db: Session, id_musica: int, indice_frase: int):
    return db.query(models.Frase).filter_by(id_musica=id_musica, indice_frase=indice_frase).first()

def buscar_frase_por_indice(db: Session, id_musica: int, indice_frase: int):
    return db.query(models.Frase).filter(
        models.Frase.id_musica == id_musica,
        models.Frase.indice_frase == indice_frase
    ).first()

def deletar_frase(db: Session, id_musica: int, indice_frase: int):
    frase = buscar_frase(db, id_musica, indice_frase)
    if frase:
        db.delete(frase)
        db.commit()
    return frase

# ===================== FRASE-PALAVRA =====================
# A função agora recebe id_musica e indice_frase para identificar a frase
def criar_frase_palavra(db: Session, id_musica: int, indice_frase: int, id_palavra: int, indice_palavra: int):
    # Passa todos os parâmetros para verificar a existência
    associacao_existente = existe_frase_palavra(db, id_musica, indice_frase, id_palavra, indice_palavra)
    if associacao_existente:
        return associacao_existente # Retorna a associação existente se já existe

    associacao = models.FrasePalavra(
        id_musica=id_musica,
        indice_frase=indice_frase,
        id_palavra=id_palavra,
        indice_palavra=indice_palavra
    )
    db.add(associacao)
    db.commit()
    db.refresh(associacao)
    return associacao

# A função agora recebe id_musica e indice_frase para identificar a frase
def existe_frase_palavra(db: Session, id_musica: int, indice_frase: int, id_palavra: int, indice_palavra: int):
    # Filtra usando a chave composta da Frase
    return db.query(models.FrasePalavra).filter_by(
        id_musica=id_musica,
        indice_frase=indice_frase,
        id_palavra=id_palavra,
        indice_palavra=indice_palavra
    ).first()

