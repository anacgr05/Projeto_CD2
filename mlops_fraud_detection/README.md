# Aula 02 - e03 Dados Sintéticos e MLOps

Este módulo apresenta um fluxo simplificado de **MLOps** para detecção de fraude com dados sintéticos.

## Visão geral

O projeto cobre as etapas principais de um mini pipeline:

1. geração de dados sintéticos
2. treinamento de modelo de classificação
3. serialização do artefato em `artifacts/model.pkl`
4. validação do modelo serializado
5. serving de predição via API FastAPI

## Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- NumPy
- Pandas
- Scikit-learn
- Joblib
- Hugging Face Hub (conceito / integração)

## Como usar

1. Acesse a pasta do módulo:
   ```bash
   cd mlops_fraud_detection
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Treine o modelo e gere o artefato:
   ```bash
   python train.py
   ```
4. Execute a API de predição:
   ```bash
   uvicorn main:app --reload --port 8001
   ```
5. Acesse `http://127.0.0.1:8001/docs` para testar a rota `/ml/predict`.

## Notebooks e passo a passo

O notebook com as respostas e o passo a passo está em:

- `notebooks/CDIA_CD2_2026_e03_dados_sinteticos_respostas.ipynb`

## Observações

- O código principal da API está em `main.py`.
- O treinamento do modelo está em `train.py`.
- O gerador de dados está em `data_utils.py`.
- O modelo é salvo em `artifacts/model.pkl`.
