import os
import pytest
import numpy as np

REPO_ID = os.getenv("HF_REPO_ID", "anaclaragr05/mlops-fraud-v1")
N_FEATURES = 5


@pytest.fixture(scope="module")
def modelo():
    """
    Carrega o modelo uma única vez para todos os testes deste módulo.
    """
    from model_utils import load_model

    return load_model(REPO_ID)


@pytest.fixture
def amostra_valida():
    """
    Amostra com valores plausíveis para o domínio do modelo.
    """
    return np.array([[150.0, 14, 5.0, 1, 0]])


PAYLOAD_VALIDO = {
    "valor_transacao": 150.0,
    "hora_transacao": 14,
    "distancia_ultima_compra": 5.0,
    "tentativas_senha": 1,
    "pais_diferente": 0,
}


@pytest.mark.integracao
def test_modelo_carregado_nao_e_none(modelo):
    assert modelo is not None


@pytest.mark.integracao
def test_modelo_tem_metodo_predict(modelo):
    assert hasattr(modelo, "predict")
    assert callable(modelo.predict)


@pytest.mark.integracao
def test_modelo_tem_metodo_predict_proba(modelo):
    assert hasattr(modelo, "predict_proba")
    assert callable(modelo.predict_proba)


@pytest.mark.integracao
def test_predict_retorna_array_com_formato_correto(modelo, amostra_valida):
    resultado = modelo.predict(amostra_valida)
    assert resultado.shape == (1,)
    assert resultado[0] in [0, 1]


@pytest.mark.integracao
def test_predict_proba_retorna_probabilidades_validas(modelo, amostra_valida):
    probas = modelo.predict_proba(amostra_valida)
    assert probas.shape == (1, 2)
    assert abs(probas[0].sum() - 1.0) < 1e-6
    assert all(0 <= p <= 1 for p in probas[0])


@pytest.mark.integracao
def test_predict_retorna_200(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200


@pytest.mark.integracao
def test_predict_retorna_campos_esperados(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    assert response.status_code == 200
    dados = response.json()
    assert "prediction" in dados
    assert "probability" in dados
    assert "label" in dados
    assert "model_version" in dados


@pytest.mark.integracao
def test_predict_prediction_e_binario(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    prediction = response.json()["prediction"]
    assert prediction in [0, 1]


@pytest.mark.integracao
def test_predict_probability_entre_zero_e_um(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    probability = response.json()["probability"]
    assert isinstance(probability, float)
    assert 0.0 <= probability <= 1.0


@pytest.mark.integracao
def test_predict_label_e_string_nao_vazia(client):
    response = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    label = response.json()["label"]
    assert isinstance(label, str)
    assert len(label) > 0


@pytest.mark.integracao
def test_predict_sem_campo_obrigatorio_retorna_422(client):
    payload_incompleto = {"valor_transacao": 120.0}
    response = client.post("/ml/predict", json=payload_incompleto)
    assert response.status_code == 422


@pytest.mark.integracao
@pytest.mark.parametrize(
    "campo,valor_invalido",
    [
        ("hora_transacao", 25),
        ("hora_transacao", -1),
        ("tentativas_senha", 0),
        ("valor_transacao", -50.0),
    ],
)
def test_predict_campo_invalido_retorna_422(client, campo, valor_invalido):
    payload = {**PAYLOAD_VALIDO, campo: valor_invalido}
    response = client.post("/ml/predict", json=payload)
    assert response.status_code == 422


@pytest.mark.integracao
def test_modelo_distingue_casos_extremos(client):
    caso_tipico = {
        "valor_transacao": 55.0,
        "hora_transacao": 13,
        "distancia_ultima_compra": 3.0,
        "tentativas_senha": 1,
        "pais_diferente": 0,
    }

    caso_suspeito = {
        "valor_transacao": 8900.0,
        "hora_transacao": 2,
        "distancia_ultima_compra": 450.0,
        "tentativas_senha": 6,
        "pais_diferente": 1,
    }

    resp_tipico = client.post("/ml/predict", json=caso_tipico)
    resp_suspeito = client.post("/ml/predict", json=caso_suspeito)

    assert resp_tipico.status_code == 200
    assert resp_suspeito.status_code == 200

    prob_tipico = resp_tipico.json()["probability"]
    prob_suspeito = resp_suspeito.json()["probability"]

    assert prob_suspeito > prob_tipico


@pytest.mark.integracao
def test_modelo_e_deterministico(client):
    resp_1 = client.post("/ml/predict", json=PAYLOAD_VALIDO)
    resp_2 = client.post("/ml/predict", json=PAYLOAD_VALIDO)

    assert resp_1.json()["prediction"] == resp_2.json()["prediction"]
    assert resp_1.json()["probability"] == resp_2.json()["probability"]
