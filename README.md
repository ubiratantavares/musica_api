# Projeto musica_api

Este é um projeto desenvolvido para criação de uma API para gerenciamento de letras de músicas, com armazenamento otimizado de palavras.

## 1. Definição do Modelo de Dados

✔  O SGBD escolhido foi o PostgreSQL

✔  Abaixo a descrição das tabelas do banco de dados **db_letras**

- Tabela **musica**:

| Campo | Descrição |
| ----- | --------- |

- Tabela **artista**:

| Campo | Descrição |
| ----- | --------- |

- Tabela **palavra**:

| Campo | Descrição |
| ----- | --------- |

- Tabela **interprete**:

| Campo | Descrição |
| ----- | --------- |

- Tabela **frase**:

| Campo | Descrição |
| ----- | --------- |

- Tabela **frase_palavra**:

| Campo | Descrição |
| ----- | --------- |

## 2. Configuração do Ambiente 

Pré-requisitos:

✔ Python 3.11+

✔ PostgreSQL instalado

✔ Ferramentas: FastAPI, SQLAlchemy, Alembic (migrations), psycopg2-binary

### 2.1 Criação do arquivo requirements.txt

✔  Arquivo **requirements.txt** contém todas as dependências necessárias;

✔ O script de instalação garante rápida configuração do ambiente Conda;

✔ Ideal para ambientes de desenvolvimento limpos e reprodutíveis.


### 2.2 Explicação das dependências

| Biblioteca	    | Função                                         |
| ------------      | ------                                         |
| fastapi	        | Framework web para criação da API              |
| uvicorn[standard]	| Servidor ASGI recomendado para rodar FastAPI   |
| sqlalchemy>=2.0	| ORM para manipulação do banco de dados         |
| psycopg2-binary   | Driver para conexão com PostgreSQL             |
| pydantic	        | Validação de dados (usado nos esquemas da API) |
| alembic	        | Ferramenta de migrations do banco              |
| python-dotenv	    | Gerenciamento de variáveis de ambiente         |

## 2.3 Criação do arquivo shell script para configuração do ambiente environment Conda

✔  Automatização do processo de configuração do ambiente Conda.

✔  Arquivo **setup_env.sh**

## 2.4 Instalação das Dependências

```shell
chmod +x setup_env.sh
./setup_env.sh
```

## 3. Criando o Banco de Dados

```shell
sudo -u postgres createdb db_letras;
```

ou acessando o console do PostgreSQL:

```shell
sudo -u postgres psql
```

✔  Para criar o banco de dados, digite no console:

```sql
CREATE DATABASE db_letra;
```

✔  Para listar todos os bancos de dados, digite no console:

```sql
\l
```

✔ Para conectar-se ao banco de dados

```sql
\c db_letras
```

✔ Para listar todas as tabelas, digite no console:

```sql
\dt
```

✔ Para visualizar a estrutura de uma tabela, digite no console:

```sql
\d musica;
```

✔  Para sair do console do PostgreSQL, digite:

```sql
\q
```

## 4. Estrutura FastAPI

```shell
musica_api/
├── alembic/                  # Pasta de migrações do Alembic
│   ├── versions/             # Arquivos de versões gerados
│   └── env.py
├── alembic.ini               # Configuração do Alembic
├── letras/                   # Diretório com os arquivos .txt das letras
├── importar_letras.py        # Script para importar as letras no banco
├── requirements.txt          # Bibliotecas Python do projeto
├── .env                      # Arquivo com variáveis de ambiente (opcional)
├── README.md                  # Descrição do projeto
├── app/                      # Pacote principal da aplicação
│   ├── __init__.py
│   ├── main.py               # Instância do FastAPI e endpoints
│   ├── database.py           # Configuração do banco de dados
│   ├── models.py             # Definição dos modelos SQLAlchemy
│   ├── schemas.py            # Pydantic schemas
│   ├── crud.py               # Operações de CRUD
│   ├── utils/
│   │   ├── __init__.py
│   │   └── import_utils.py   # Funções auxiliares para importação
│   └── routers/
│       ├── __init__.py
│       ├── artista.py        # Endpoints de artista
│       ├── musica.py         # Endpoints de música
│       ├── palavra.py        # Endpoints de palavra
│       ├── interpretacao.py  # Endpoints de interpretação
│       └── frase.py          # Endpoints de frase
└── .gitignore

```

## 5. Configuração do Banco de Dados

* Script **database.py**


## 6. Estrutura dos Modelos SQLAlchemy

* Script **models.py**

## 7. Configurando o Alembic para Migrations

### 7.1 Pré-Requisitos

Certifique-se de que já possui:

✔ Ambiente Python criado (conda ou venv)

✔ Bibliotecas instaladas: alembic, sqlalchemy, psycopg2-binary

✔ O arquivo **database.py** configurado com a conexão para o PostgreSQL

✔ Modelos SQLAlchemy no arquivo **models.py**

### 7.2 Inicializar o Alembic no Projeto

✔ Execute no terminal, dentro da pasta raiz do seu projeto:

```shell
alembic init alembic
```

O comando acima cria a seguinte estrutura:

```shell
alembic/
│   env.py         # Arquivo principal de configuração do Alembic
│   script.py.mako # Template dos scripts de migration
└── versions/      # Onde ficarão as migrations geradas

alembic.ini        # Configuração global do Alembic
```

### 7.3 Configurando o arquivo alembic.ini

Abra o arquivo alembic.ini e edite a linha da URL de conexão para o banco:

```iini
sqlalchemy.url = postgresql+psycopg2://usuario:senha@localhost/letras_musicas
```

✔ Troque usuario e senha pelos dados corretos do seu banco.

### 7.4 Configurando o arquivo env.py

✔ Dentro de alembic/env.py, localize:

```python
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic import context
```

✔ Logo abaixo, importe o seu arquivo models e o Base do SQLAlchemy:

```python
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Base  # Ajuste conforme o caminho do seu projeto
```

✔ Depois, localize a linha:

```python
target_metadata = None
```

✔ E substitua por:

```python
target_metadata = Base.metadata
```

✔ Isso faz com que o Alembic reconheça os modelos para gerar migrations automáticas.

### 7.5 Gerando a primeira Migration

✔ No terminal, execute:
	
```shell
alembic revision --autogenerate -m "Criação inicial"
```

✔ O Alembic irá inspecionar os modelos e gerar um arquivo em alembic/versions/ com as instruções SQL correspondentes.

### 7.6 Aplicando a Migration no banco 

✔ Execute:

```shell
alembic upgrade head
```

### 7.7 Visualizando os histórico das Migrations

✔ Execute:

```shell
alembic history
```

✔ Sempre que modificar os modelos (models.py), gere uma nova migration executando os comandos em 7.5, 7.6 e 7.7.

## 8. Estruturando os modelos de entrada e saída

✔  Arquivo **schemas.py** define os modelos de entrada (requisições) e saída (respostas) usando Pydantic, que o FastAPI utiliza para validação e documentação automática.

## 9. Encapsulando a lógica do banco de dados para o CRUD

✔  Arquivo **crud.py** 

## 10. Criando as rotas em routers

✔  Ver arquivos na pasta routers.

## 11. Criando o script principal

* Script **main.py**

## 12. Testando a API

✔  Para testar a API, basta rodar:

```shell
uvicorn app.main:app --reload
```

✔  E acessar a documentação automática em:

http://127.0.0.1:8000/docs

## 13. Importando automaticamente as letras

✔  Arquuivo **import_letras.py**



 
