from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from models.reserva import ReservaInput, ReservaOutput

router = APIRouter()

reservas = [
    {
        "id": 1,
        "mesa": 5,
        "nome": "João",
        "pessoas": 4,
        "data_hora": "2026-07-25T20:00:00",
        "ativa": True,
        "criada_em": "2026-07-23T10:00:00",
    },
    {
        "id": 2,
        "mesa": 2,
        "nome": "Pedro",
        "pessoas": 6,
        "data_hora": "2025-04-26T19:30:00",
        "ativa": False,
        "criada_em": "2025-04-23T10:10:00",
    },
]


@router.post("/", response_model=ReservaOutput)
async def criar_reserva(reserva: ReservaInput):
    data_reserva = reserva.data_hora.date()

    conflito = any(
        r["mesa"] == reserva.mesa
        and r["ativa"]
        and datetime.fromisoformat(r["data_hora"]).date() == data_reserva
        for r in reservas
    )

    if conflito:
        raise HTTPException(
            status_code=400,
            detail=f"Mesa {reserva.mesa} já está reservada para {data_reserva}",
        )

    nova_reserva = {
        "id": len(reservas) + 1,
        "mesa": reserva.mesa,
        "nome": reserva.nome,
        "pessoas": reserva.pessoas,
        "data_hora": reserva.data_hora.isoformat(),
        "ativa": True,
        "criada_em": datetime.now().isoformat(),
    }

    reservas.append(nova_reserva)
    return nova_reserva


@router.get("/")
async def listar_reservas(data: Optional[str] = None, apenas_ativas: bool = True):
    resultado = reservas

    if apenas_ativas:
        resultado = [r for r in resultado if r["ativa"]]

    if data:
        resultado = [
            r
            for r in resultado
            if datetime.fromisoformat(r["data_hora"]).date().isoformat() == data
        ]

    return resultado


@router.get("/mesa/{numero}")
async def reservas_por_mesa(numero: int):
    return [r for r in reservas if r["mesa"] == numero]


@router.get("/{reserva_id}", response_model=ReservaOutput)
async def buscar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            return reserva

    raise HTTPException(status_code=404, detail="Reserva não encontrada")


@router.delete("/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    for reserva in reservas:
        if reserva["id"] == reserva_id:
            if not reserva["ativa"]:
                raise HTTPException(status_code=400, detail="Reserva já está cancelada")

            reserva["ativa"] = False
            return {"mensagem": "Reserva cancelada com sucesso"}

    raise HTTPException(status_code=404, detail="Reserva não encontrada")
