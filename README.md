# Projeto 1 - Ciência de Dados 2

Este repositório é a realização das atividades desenvolvidas ao longo dos cadernos da disciplina.  
O projeto foi organizado de forma evolutiva, transformando os exercícios em uma base prática de desenvolvimento com:

- **FastAPI**
- **Pydantic**
- **Pytest**
- **GitHub Actions**
- **dados sintéticos**
- **treinamento de modelo**
- **integração com Hugging Face Hub**
- **CI com testes automatizados**

---

# Visão geral do projeto

Etapas:

## 1. e02 ( aula 1 ) - API com FastAPI
Na primeira etapa, foi construída a API do restaurante **Bella Tavola**, com rotas para pratos, bebidas, pedidos e reservas.

Nessa fase, os principais conceitos trabalhados foram:

- criação de rotas
- métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`)
- `path parameters`
- `query parameters`
- `body` da requisição
- validação com Pydantic
- tratamento de erros com `HTTPException`
- organização modular com `routers/` e `models/`

## 2. e03 (aula 2) Dados sintéticos e modelo
Na segunda etapa, o foco foi construir um mini fluxo de **MLOps**, incluindo:

- geração de dados sintéticos
- treino de modelo de classificação
- serialização em `model.pkl`
- publicação no Hugging Face Hub
- carregamento do modelo
- serving via API

## 3. e04 (aula 3,4e 5) - CI, testes automatizados e integração com modelo
Na terceira etapa, o projeto evoluiu para práticas de engenharia de software mais robustas, incluindo:

- GitHub Actions
- integração contínua (CI)
- testes automatizados com `pytest`
- uso de `TestClient`
- `conftest.py` e fixtures
- parametrização de testes
- validação de contrato
- integração com modelo real
- uso de `HF_TOKEN` como secret
- cache de artefatos
- debugging de pipeline
