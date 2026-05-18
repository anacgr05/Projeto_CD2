# Bella Tavola com Docker

Este arquivo documenta a containerização da API Bella Tavola desenvolvida na Aula 1.

## Objetivo
Empacotar a API FastAPI em uma imagem Docker reproduzível, permitindo rodar a aplicação com o mesmo comportamento em diferentes ambientes.

## Arquivos principais
- `Dockerfile`
- `.dockerignore`

## Como buildar a imagem
```bash
docker build -t bella-tavola:v1 .