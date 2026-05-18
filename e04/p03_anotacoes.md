# e04 p03 — Integração com modelo e debugging

## Objetivo
Integrar o modelo publicado no Hugging Face Hub ao pipeline de CI e adicionar práticas de debugging para diagnosticar falhas com rapidez.

## O que foi implementado
- criação de `model_utils.py`
- criação do router `ml.py` com `/ml/predict` e `/ml/health`
- criação de `tests/test_modelo.py`
- configuração do secret `HF_TOKEN` no GitHub
- adição de cache do modelo no pipeline
- separação do workflow em jobs de qualidade e integração
- adição de step de diagnóstico
