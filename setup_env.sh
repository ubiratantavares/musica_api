#!/bin/bash

# Nome do ambiente Conda
ENV_NAME="musica_api"

# Cria o ambiente Conda com Python 3.11
conda create -n $ENV_NAME python=3.11 -y

# Ativa o ambiente
source $(conda info --base)/etc/profile.d/conda.sh
conda activate $ENV_NAME

# Instala as dependências
pip install -r requirements.txt

echo "Ambiente $ENV_NAME configurado com sucesso!"
