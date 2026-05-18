# e04 p02 — Testes automatizados com pytest

## Objetivo
Evoluir o workflow de CI para executar testes automatizados da API Bella Tavola com pytest.

- atualização do `requirements.txt` para incluir `pytest` e `httpx`
- criação da pasta `tests/`
- criação de `test_saude.py`
- criação de `test_pratos.py`
- criação de `test_pedidos.py`
- criação de `conftest.py` com fixture `client`
- criação de `pytest.ini` com marcadores
- atualização do GitHub Actions para rodar `pytest tests/ -v --tb=short`
