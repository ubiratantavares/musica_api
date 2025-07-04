from pydantic import BaseModel
from typing import Optional

# ====== MÚSICA ======
class MusicaCreate(BaseModel):
    titulo: str

class MusicaResponse(BaseModel):
    id: int
    titulo: str

    class Config:
        from_attributes = True  # Pydantic v2 substitui orm_mode


# ====== ARTISTA ======
class ArtistaCreate(BaseModel):
    nome: str

class ArtistaResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


# ====== INTERPRETE ======
class InterpreteCreate(BaseModel):
    id_musica: int
    id_artista: int

class InterpreteResponse(BaseModel):
    id: int
    id_musica: int
    id_artista: int

    class Config:
        from_attributes = True


# ====== FRASE ======
class FraseCreate(BaseModel):
    id_musica: int
    indice_frase: int

class FraseResponse(BaseModel):
    id_musica: int
    indice_frase: int

    class Config:
        from_attributes = True


# ====== PALAVRA ======
class PalavraCreate(BaseModel):
    vocabulo: str

class PalavraResponse(BaseModel):
    id: int
    vocabulo: str

    class Config:
        from_attributes = True


# ====== FRASE-PALAVRA ======
class FrasePalavraCreate(BaseModel):
    id_frase: int
    id_palavra: int
    indice_palavra: int

class FrasePalavraResponse(BaseModel):
    id_frase: int
    id_palavra: int
    indice_palavra: int

    class Config:
        from_attributes = True
