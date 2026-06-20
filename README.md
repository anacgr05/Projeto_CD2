# Projeto 1 - Ciência de Dados 2

Este repositório reúne as atividades práticas da disciplina em três módulos principais, com código e notebooks organizados para facilitar a navegação.

## Estrutura do projeto

- `fastapi_api/`: API FastAPI do restaurante **Bella Tavola**.
- `mlops_fraud_detection/`: fluxo de MLOps com dados sintéticos, treinamento e serving de modelo.
- `docs/`: documentação consolidada de CI e notas de aula.
- `notebooks/`: notebooks com as respostas e passo a passo de cada aula.

## Onde estão os notebooks

Todos os notebooks de resposta estão juntos em:

- `notebooks/`

Para acessar o passo a passo completo, abra o notebook correspondente e siga as células na ordem apresentada.

## Mini índice dos notebooks

- `CDIA_CD2_2026_e02_fastAPI_respostas.ipynb` — respostas e passos da Aula 1 / FastAPI.
- `CDIA_CD2_2026_e03_dados_sinteticos_respostas.ipynb` — respostas e passos da Aula 2 / MLOps e dados sintéticos.
- `CDIA_CD2_2026_e04_p01_github_actions_respostas.ipynb` — respostas da primeira parte de GitHub Actions e CI.
- `CDIA_CD2_2026_e04_p02_github_actions_respostas.ipynb` — respostas da segunda parte com testes automatizados.
- `CDIA_CD2_2026_e04_p03_github_actions_respostas.ipynb` — respostas da terceira parte sobre integração de modelo e debugging.
- `CDIA_CD2_2026_e05_p01_docker_Respostas.ipynb` — respostas do Docker parte 1.
- `CDIA_CD2_2026_e05_p02_docker_Respostas.ipynb` — respostas do Docker parte 2.
- `CDIA_CD2_2026_e05_p03_docker_Resposta.ipynb` — respostas do Docker parte 3.

## Notas de CI e GitHub Actions

A documentação consolidada para a aula e04 está em `docs/e04_notes.md`.

## Como usar este repositório

1. Leia o notebook da aula em `notebooks/...` para entender o fluxo e os passos.
2. Verifique os arquivos de código na pasta correspondente à aula.
3. Siga as instruções do README específico de cada módulo.

## Resumo das aulas

### Aula 1 / e02 — FastAPI
- Construção de uma API para o restaurante **Bella Tavola**.
- Rotas para pratos, bebidas, pedidos e reservas.
- Validação com `Pydantic`.
- Organização modular com `routers/` e `models/`.
- Dockerização disponível em `fastapi_api/README_docker.md`.

### Aula 2 / e03 — MLOps e dados sintéticos
- Geração de dados sintéticos de fraude.
- Treinamento e serialização de modelo.
- Exposição de predição via API.
- Arquivos principais: `train.py`, `main.py`, `model_utils.py`, `data_utils.py`.

### Aula 3 / e04 — GitHub Actions e CI
- Materiais para workflow de integração contínua.
- Testes automatizados com `pytest`.
- Notebooks e anotações para os exercícios de CI.

## Nota

Os notebooks organizam o passo a passo e as respostas. Use-os como guia principal antes de executar os códigos do projeto.
