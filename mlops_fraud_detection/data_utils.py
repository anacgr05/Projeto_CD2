from typing import Tuple
import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "valor_transacao",
    "hora_transacao",
    "distancia_ultima_compra",
    "tentativas_senha",
    "pais_diferente",
]

TARGET_COLUMN = "target"


def gerar_dataset(
    n_samples: int = 1000,
    seed: int = 42,
    proporcao_positivos: float = 0.3
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Gera dataset sintético para detecção de fraude.

    Parâmetros
    ----------
    n_samples : int
        Número de amostras a gerar.
    seed : int
        Seed para reprodutibilidade.
    proporcao_positivos : float
        Proporção da classe positiva. Deve estar entre 0.05 e 0.95.

    Retorna
    -------
    df : pd.DataFrame
        Dataset completo com features e target.
    X : np.ndarray
        Matriz de features.
    y : np.ndarray
        Vetor de targets.
    """
    if not (0.05 <= proporcao_positivos <= 0.95):
        raise ValueError(
            f"proporcao_positivos deve estar entre 0.05 e 0.95, recebido: {proporcao_positivos}"
        )

    rng = np.random.default_rng(seed)

    fraude = rng.choice(
        [0, 1],
        size=n_samples,
        p=[1 - proporcao_positivos, proporcao_positivos]
    )

    valor_transacao = np.where(
        fraude == 1,
        rng.uniform(500, 10000, n_samples),
        rng.uniform(10, 800, n_samples)
    ).round(2)

    hora_transacao = np.where(
        fraude == 1,
        rng.integers(0, 6, n_samples),
        rng.integers(7, 23, n_samples)
    )

    distancia_ultima_compra = np.where(
        fraude == 1,
        rng.uniform(100, 5000, n_samples),
        rng.uniform(0, 50, n_samples)
    ).round(1)

    tentativas_senha = np.where(
        fraude == 1,
        rng.integers(2, 10, n_samples),
        rng.integers(1, 2, n_samples)
    )

    pais_diferente = (
        rng.random(n_samples) < np.where(fraude == 1, 0.40, 0.05)
    ).astype(int)

    df = pd.DataFrame({
        "valor_transacao": valor_transacao,
        "hora_transacao": hora_transacao,
        "distancia_ultima_compra": distancia_ultima_compra,
        "tentativas_senha": tentativas_senha,
        "pais_diferente": pais_diferente,
        TARGET_COLUMN: fraude
    })

    X = df[FEATURE_COLUMNS].values
    y = df[TARGET_COLUMN].values

    return df, X, y