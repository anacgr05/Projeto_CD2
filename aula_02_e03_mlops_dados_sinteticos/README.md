# e03 - Dados Sintéticos, Serialização e Serving de Modelo

Este projeto foi desenvolvido com foco em um fluxo simplificado de **MLOps**: geração de dados sintéticos, treinamento de modelo, serialização do artefato, publicação no Hugging Face Hub e consumo do modelo por meio de uma API FastAPI.

## Visão geral

A proposta desta aula foi simular um cenário de **detecção de fraude em transações** sem depender de dados reais. Para isso, o projeto foi dividido em etapas que representam um pipeline completo:

1. geração de dados sintéticos com variáveis de domínio  
2. treinamento de um modelo de classificação  
3. salvamento do modelo em arquivo `.pkl`  
4. publicação do artefato no Hugging Face Hub  
5. carregamento remoto do modelo  
6. exposição de predição via API

## Tecnologias utilizadas

Python
FastAPI
Uvicorn
NumPy
Pandas
Scikit-learn
Joblib
Hugging Face Hub
Objetivos da aula
