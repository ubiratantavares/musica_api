from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from . import models, schemas, crud
from sqlalchemy import text

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def testar_conexao():
    try:
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
        print("Conexão com o banco de dados estabelecida com sucesso.")
    except Exception as e:
        print("Falha ao tentar conectar com o banco de dados.")

# Criar uma música
@app.post("/musicas/", response_model=schemas.MusicaResponse)
def criar_musica(musica: schemas.MusicaCreate, db: Session = Depends(get_db)):
    return crud.criar_musica(db, musica)

# Listar músicas
@app.get("/musicas/", response_model=list[schemas.MusicaResponse])
def listar_musicas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_musicas(db, skip, limit)

# Buscar música por ID
@app.get("/musicas/{musica_id}", response_model=schemas.MusicaResponse)
def buscar_musica(musica_id: int, db: Session = Depends(get_db)):
    musica = crud.buscar_musica(db, musica_id)
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return musica

# Deletar música por ID
@app.delete("/musicas/{musica_id}", response_model=schemas.MusicaResponse)
def deletar_musica(musica_id: int, db: Session = Depends(get_db)):
    musica = crud.deletar_musica(db, musica_id)
    if not musica:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return musica

# Criar uma artista
@app.post("/artistas/", response_model=schemas.ArtistaResponse)
def criar_artista(artista: schemas.ArtistaCreate, db: Session = Depends(get_db)):
    return crud.criar_artista(db, artista)

# Listar artistas
@app.get("/artistas/", response_model=list[schemas.ArtistaResponse])
def listar_artistas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_artistas(db, skip, limit)

# Buscar artista por ID
@app.get("/artistas/{artista_id}", response_model=schemas.ArtistaResponse)
def buscar_artista(artista_id: int, db: Session = Depends(get_db)):
    artista = crud.buscar_artista(db, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado")
    return artista

# Deletar artista por ID
@app.delete("/artistas/{artista_id}", response_model=schemas.ArtistaResponse)
def deletar_artista(artista_id: int, db: Session = Depends(get_db)):
    artista = crud.deletar_artista(db, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado")
    return artista

# Criar um palavra
@app.post("/palavras/", response_model=schemas.PalavraResponse)
def criar_palavra(palavra: schemas.PalavraCreate, db: Session = Depends(get_db)):
    palavra_existente = crud.buscar_palavra_por_texto(db, palavra.texto)

    if palavra_existente:
        raise HTTPException(status_code = 409, detail = "Palavra já cadastrada.")
        
    return crud.criar_palavra(db, palavra)

# Listar palavras
@app.get("/palavras/", response_model=list[schemas.PalavraResponse])
def listar_palavras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_palavras(db, skip, limit)

# Buscar palavra por ID
@app.get("/palavras/{palavra_id}", response_model=schemas.PalavraResponse)
def buscar_palavra(palavra_id: int, db: Session = Depends(get_db)):
    palavra = crud.buscar_palavra(db, palavra_id)
    if not palavra:
        raise HTTPException(status_code=404, detail="Palavra não encontrada")
    return palavra

# Deletar palavra por ID
@app.delete("/palavras/{palavra_id}", response_model=schemas.PalavraResponse)
def deletar_palavra(palavra_id: int, db: Session = Depends(get_db)):
    palavra = crud.deletar_palavra(db, palavra_id)
    if not palavra:
        raise HTTPException(status_code=404, detail="Palavra não encontrada")
    return palavra

# Criar interpretação
@app.post("/interpretacoes/", response_model=schemas.InterpretacaoResponse)
def criar_interpretacao(interpretacao: schemas.InterpretacaoCreate, db: Session = Depends(get_db)):
    return crud.criar_interpretacao(db, interpretacao)


# Listar interpretações
@app.get("/interpretacoes/", response_model=list[schemas.InterpretacaoResponse])
def listar_interpretacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_interpretacoes(db, skip, limit)


# Buscar interpretação por ID
@app.get("/interpretacoes/{interpretacao_id}", response_model=schemas.InterpretacaoResponse)
def buscar_interpretacao(interpretacao_id: int, db: Session = Depends(get_db)):
    interpretacao = crud.buscar_interpretacao(db, interpretacao_id)
    if not interpretacao:
        raise HTTPException(status_code=404, detail="Interpretação não encontrada")
    return interpretacao


# Deletar interpretação
@app.delete("/interpretacoes/{interpretacao_id}", response_model=schemas.InterpretacaoResponse)
def deletar_interpretacao(interpretacao_id: int, db: Session = Depends(get_db)):
    interpretacao = crud.deletar_interpretacao(db, interpretacao_id)
    if not interpretacao:
        raise HTTPException(status_code=404, detail="Interpretação não encontrada")
    return interpretacao

# Criar frase
@app.post("/frases/", response_model=schemas.FraseResponse)
def criar_frase(frase: schemas.FraseCreate, db: Session = Depends(get_db)):
    return crud.criar_frase(db, frase)


# Listar frases
@app.get("/frases/", response_model=list[schemas.FraseResponse])
def listar_frases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_frases(db, skip, limit)


# Buscar frase por ID
@app.get("/frases/{frase_id}", response_model=schemas.FraseResponse)
def buscar_frase(frase_id: int, db: Session = Depends(get_db)):
    frase = crud.buscar_frase(db, frase_id)
    if not frase:
        raise HTTPException(status_code=404, detail="Frase não encontrada")
    return frase


# Deletar frase
@app.delete("/frases/{frase_id}", response_model=schemas.FraseResponse)
def deletar_frase(frase_id: int, db: Session = Depends(get_db)):
    frase = crud.deletar_frase(db, frase_id)
    if not frase:
        raise HTTPException(status_code=404, detail="Frase não encontrada")
    return frase
