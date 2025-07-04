import os
import re
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas
from app.utils import import_utils

DIRETORIO_LETRAS = "letras"
LIMPA_PONTUACAO = re.compile(r"[^\wáéíóúãõâêîôûçÁÉÍÓÚÃÕÂÊÎÔÛÇ]+")


def extrair_titulo(nome_arquivo: str) -> str:
    nome_arquivo = nome_arquivo.replace(".txt", "").strip()
    if " - " not in nome_arquivo:
        raise ValueError(f"Formato inválido do nome do arquivo: {nome_arquivo}")
    titulo, _ = nome_arquivo.split(" - ", 1)
    return titulo.strip()


def extrair_artistas(nome_arquivo: str) -> list[str]:
    nome_arquivo = nome_arquivo.replace(".txt", "").strip()
    if " - " not in nome_arquivo:
        raise ValueError(f"Formato inválido do nome do arquivo: {nome_arquivo}")
    _, artistas_str = nome_arquivo.split(" - ", 1)
    artistas = [art.strip() for art in artistas_str.split(" e ") if art.strip()]
    if not artistas:
        raise ValueError(f"Não foi possível extrair os artistas do arquivo: {nome_arquivo}")
    return artistas


def processar_frase(db: Session, musica_id: int, frase_texto: str, indice_frase: int):
    frase = crud.buscar_frase_por_indice(db, musica_id, indice_frase)
    if not frase:
        frase = crud.criar_frase(db, schemas.FraseCreate(id_musica=musica_id, indice_frase=indice_frase))

    palavras = LIMPA_PONTUACAO.sub(" ", frase_texto).lower().split()

    for indice_palavra, vocabulo in enumerate(palavras, start=1):
        palavra = import_utils.buscar_ou_criar_palavra(db, vocabulo)
        # CHAMA AGORA COM id_musica e indice_frase da frase
        if not crud.existe_frase_palavra(db, frase.id_musica, frase.indice_frase, palavra.id, indice_palavra):
            crud.criar_frase_palavra(db, frase.id_musica, frase.indice_frase, palavra.id, indice_palavra)

def processar_arquivo(db: Session, caminho: str):
    print(f"Processando arquivo: {caminho}")

    titulo = extrair_titulo(os.path.basename(caminho))
    musica = import_utils.buscar_ou_criar_musica(db, titulo)

    nomes_artistas = extrair_artistas(os.path.basename(caminho))
    frases = ler_frases_arquivo(caminho)

    for nome in nomes_artistas:
        artista = import_utils.buscar_ou_criar_artista(db, nome)
        interprete = import_utils.buscar_ou_criar_interprete(db, musica.id, artista.id)

    for indice_frase, frase_texto in enumerate(frases, start=1):
        processar_frase(db, musica.id, frase_texto, indice_frase)

    db.commit()
    print(f"Arquivo '{caminho}' processado com sucesso.")


def ler_frases_arquivo(caminho: str) -> list[str]:
    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]


def processar_todos_arquivos():
    db = SessionLocal()

    try:
        arquivos_txt = [f for f in os.listdir(DIRETORIO_LETRAS) if f.endswith(".txt")]
        for arquivo in arquivos_txt:
            caminho = os.path.join(DIRETORIO_LETRAS, arquivo)
            try:
                processar_arquivo(db, caminho)
            except Exception as e:
                print(f"Erro ao processar '{arquivo}': {e}")
                db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    processar_todos_arquivos()
