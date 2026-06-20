from pathlib import Path
import os
import joblib
import numpy as np
import sklearn
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from data_utils import gerar_dataset, FEATURE_COLUMNS


ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)


def treinar_modelo(
    n_samples: int = 2000,
    seed: int = 42,
    proporcao_positivos: float = 0.30
):
    df, X, y = gerar_dataset(
        n_samples=n_samples,
        seed=seed,
        proporcao_positivos=proporcao_positivos
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=seed,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=seed
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    report_text = classification_report(
        y_test,
        y_pred,
        target_names=["legitimo", "fraude"]
    )
    report_dict = classification_report(
        y_test,
        y_pred,
        target_names=["legitimo", "fraude"],
        output_dict=True
    )

    print("=== CLASSIFICATION REPORT ===")
    print(report_text)

    model_path = ARTIFACTS_DIR / "model.pkl"
    joblib.dump(model, model_path)

    tamanho_kb = os.path.getsize(model_path) / 1024
    print(f"\nModelo salvo em: {model_path} ({tamanho_kb:.2f} KB)")

    model_carregado = joblib.load(model_path)
    amostra = X_test[:5]

    pred_original = model.predict(amostra)
    pred_carregado = model_carregado.predict(amostra)

    assert np.array_equal(pred_original, pred_carregado), "Predições divergem!"
    print("✅ Artefato validado com sucesso")

    requirements_model = (
        f"scikit-learn=={sklearn.__version__}\n"
        f"joblib=={joblib.__version__}\n"
        f"numpy=={np.__version__}\n"
        f"pandas=={pd.__version__}\n"
    )
    (ARTIFACTS_DIR / "requirements_model.txt").write_text(
        requirements_model,
        encoding="utf-8"
    )

    precision_fraude = report_dict["fraude"]["precision"]
    recall_fraude = report_dict["fraude"]["recall"]
    f1_fraude = report_dict["fraude"]["f1-score"]

    model_card = f"""---
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

{FEATURE_COLUMNS}

## Métricas

- Precision (fraude): {precision_fraude:.4f}
- Recall (fraude): {recall_fraude:.4f}
- F1-score (fraude): {f1_fraude:.4f}

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
"""
    
    (ARTIFACTS_DIR / "model_card.md").write_text(
        model_card,
        encoding="utf-8"
    )

    return {
        "model": model,
        "model_path": str(model_path),
        "report_text": report_text,
        "precision_fraude": precision_fraude,
        "recall_fraude": recall_fraude,
        "f1_fraude": f1_fraude
    }


if __name__ == "__main__":
    resultado = treinar_modelo()
    print("\n✅ Pipeline de treino concluído")