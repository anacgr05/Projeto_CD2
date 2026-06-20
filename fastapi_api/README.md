# Aula 01 - e02 FastAPI

Este módulo implementa a primeira prática da disciplina, criando uma API para o restaurante fictício **Bella Tavola**.

## Objetivo

Desenvolver uma API FastAPI de forma progressiva e organizada, com rotas REST para:

- pratos
- bebidas
- pedidos
- reservas

O projeto utiliza:

- FastAPI
- Pydantic
- tratamento de exceções
- modularização com `routers/` e `models/`
- configuração com `config.py` e `.env`

## Como usar

1. Acesse a pasta deste módulo:
   ```bash
   cd fastapi_api
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode a API localmente:
   ```bash
   uvicorn main:app --reload
   ```
4. Abra o navegador em `http://127.0.0.1:8000/docs`.

## Notebooks e passo a passo

O notebook com as respostas e o fluxo passo a passo está em:

- `notebooks/CDIA_CD2_2026_e02_fastAPI_respostas.ipynb`

## Docker

A documentação de Docker está em `README_docker.md`.

## Observações

- O código principal está em `main.py`.
- A configuração da API fica em `config.py`.
- As rotas estão em `routers/`.
- Os modelos de dados estão em `models/`.

