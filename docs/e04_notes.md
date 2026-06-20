# e04 — GitHub Actions, CI e Testes

Esta documentação reúne todas as notas e anotações da aula e04 em um único arquivo.

## Visão geral

O objetivo desta etapa é validar e automatizar o projeto do restaurante **Bella Tavola** com:

- GitHub Actions
- integração contínua (CI)
- testes automatizados com `pytest`
- validação de endpoints da API
- diagnóstico de falhas
- integração de modelo de machine learning

## Conteúdo consolidado

### 1. Workflow de CI básico

O workflow executa:

1. baixar o código do repositório
2. configurar Python 3.11
3. instalar dependências
4. subir a API com Uvicorn
5. testar se a rota raiz responde corretamente

### 2. Testes automatizados com pytest

A evolução do pipeline incluiu:

- adição de `pytest` e `httpx` ao ambiente
- criação da pasta `tests/`
- criação de testes para saúde da API, pratos e pedidos
- configuração de `conftest.py` com fixture `client`
- criação de `pytest.ini` com marcadores
- execução do workflow de CI com `pytest tests/ -v --tb=short`

### 3. Integração com modelo e debug

A fase final abordou:

- criação de `model_utils.py`
- implementação do router `ml.py` com rotas `/ml/predict` e `/ml/health`
- criação de `tests/test_modelo.py`
- uso do secret `HF_TOKEN` no GitHub Actions
- cache de modelo para acelarar o pipeline
- separação de jobs e adicionamento de passos de diagnóstico para falhas

## Notebooks relacionados ao e04

- `notebooks/CDIA_CD2_2026_e04_p01_github_actions_respostas.ipynb`
- `notebooks/CDIA_CD2_2026_e04_p02_github_actions_respostas.ipynb`
- `notebooks/CDIA_CD2_2026_e04_p03_github_actions_respostas.ipynb`

## Como usar

1. Abra os notebooks do e04 para ver as respostas completas e o passo a passo.
2. Consulte este arquivo para entender a consolidação do conteúdo de CI, testes e integração de modelo.
3. Use `docs/e04_notes.md` como referência principal para a aula e04.
