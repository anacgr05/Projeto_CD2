from fastapi import APIRouter, HTTPException

from models.pedido import PedidoInput, PedidoOutput
from routers.pratos import pratos

router = APIRouter()

pedidos = []


@router.get("/")
async def listar_pedidos():
    return pedidos


@router.post("/", response_model=PedidoOutput)
async def criar_pedido(pedido: PedidoInput):
    prato = next((p for p in pratos if p["id"] == pedido.prato_id), None)

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    if not prato["disponivel"]:
        raise HTTPException(
            status_code=400,
            detail=f"O prato '{prato['nome']}' não está disponível no momento",
        )

    valor_unitario = (
        prato["preco_promocional"] if prato.get("preco_promocional") else prato["preco"]
    )

    novo_id = len(pedidos) + 1
    novo_pedido = {
        "id": novo_id,
        "prato_id": pedido.prato_id,
        "nome_prato": prato["nome"],
        "quantidade": pedido.quantidade,
        "valor_unitario": valor_unitario,
        "valor_total": round(valor_unitario * pedido.quantidade, 2),
        "observacao": pedido.observacao,
    }

    pedidos.append(novo_pedido)
    return novo_pedido
