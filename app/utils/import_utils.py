from sqlalchemy.orm import Session
from app import crud, schemas

# ===================== MÚSICA =====================
def buscar_ou_criar_musica(db: Session, titulo: str):
    musica = crud.buscar_musica_por_titulo(db, titulo)
    if musica:
        return musica
    return crud.criar_musica(db, schemas.MusicaCreate(titulo=titulo))


# ===================== ARTISTA =====================
def buscar_ou_criar_artista(db: Session, nome: str):
    artista = crud.buscar_artista_por_nome(db, nome)
    if artista:
        return artista
    return crud.criar_artista(db, schemas.ArtistaCreate(nome=nome))


# ===================== INTERPRETE =====================
def buscar_ou_criar_interprete(db: Session, musica_id: int, artista_id: int):
    interprete = crud.buscar_interprete_por_musica_artista(db, musica_id, artista_id)
    if interprete:
        return interprete
    return crud.criar_interprete(db, schemas.InterpreteCreate(id_musica=musica_id, id_artista=artista_id))


# ===================== PALAVRA =====================
def buscar_ou_criar_palavra(db: Session, vocabulo: str):
    vocabulo = vocabulo.lower().strip()
    palavra = crud.buscar_palavra_por_vocabulo(db, vocabulo)
    if palavra:
        return palavra
    return crud.criar_palavra(db, schemas.PalavraCreate(vocabulo=vocabulo))
