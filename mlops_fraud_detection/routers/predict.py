import os
import numpy as np

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from data_utils import FEATURE_COLUMNS
from model_utils import load_model

router = APIRouter()

MODEL_REPO_ID = os.getenv("HF_REPO_ID", "")
MODEL_FILENAME = os.getenv("HF_MODEL_FILENAME", "model.pkl")

_model = None


def get_model():
    global _model

    if _model is None:
        if not MODEL_REPO_ID:
            raise RuntimeError("HF_REPO_ID não configurado")
        _model = load_model(
            repo_id=MODEL_REPO_ID,
            filename=MODEL_FILENAME
        )
    return _model


class PredictInput(BaseModel):
    valor_transacao: float = Field(gt=0, description="Valor em reais")
    hora_transacao: int = Field(ge=0, le=23, description="Hora do dia")
    distancia_ultima_compra: float = Field(ge=0, description="Distância em km")
    tentativas_senha: int = Field(ge=1, description="Tentativas de senha")
    pais_diferente: int = Field(ge=0, le=1, description="1 se país diferente")


class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str


@router.post("/predict", response_model=PredictOutput)
async def predict(input_data: PredictInput):
    try:
        model = get_model()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Modelo indisponível: {e}")

    payload = input_data.model_dump()
    features = np.array([[payload[col] for col in FEATURE_COLUMNS]], dtype=float)

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    label = "fraude" if prediction == 1 else "legitimo"

    return PredictOutput(
        prediction=prediction,
        probability=round(probability, 4),
        label=label,
        model_version=MODEL_REPO_ID
    )


@router.get("/health")
async def health():
    try:
        model = get_model()
        test_input = np.zeros((1, len(FEATURE_COLUMNS)))
        model.predict(test_input)

        return {
            "api": "ok",
            "model": "ok",
            "model_repo": MODEL_REPO_ID
        }

    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "api": "ok",
                "model": "degraded",
                "model_repo": str(e)
            }
        )