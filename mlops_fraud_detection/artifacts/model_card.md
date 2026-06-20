---
language: pt
tags:
  - sklearn
  - classification
  - fraud-detection
  - mlops
---

# mlops-fraud-v1

Modelo de classificação binária para detecção de transações potencialmente fraudulentas.

## Objetivo

Este modelo foi treinado com dados sintéticos para fins educacionais, simulando um cenário de detecção de fraude em transações financeiras.

## Features de entrada

- valor_transacao
- hora_transacao
- distancia_ultima_compra
- tentativas_senha
- pais_diferente

## Ordem das features

['valor_transacao', 'hora_transacao', 'distancia_ultima_compra', 'tentativas_senha', 'pais_diferente']

## Métricas

- Precision (fraude): 1.0000
- Recall (fraude): 1.0000
- F1-score (fraude): 1.0000

## Limitações

- O dataset é sintético e simplificado.
- As distribuições não representam todas as complexidades do mundo real.
- O modelo não foi calibrado para produção real.

## Exemplo de uso

```python
from huggingface_hub import hf_hub_download
import joblib

path = hf_hub_download(repo_id="SEU_USUARIO/mlops-fraud-v1", filename="model.pkl")
model = joblib.load(path)

features = [[250.0, 14, 12.5, 1, 0]]
prediction = model.predict(features)
print(prediction)
