import os
import time
from datetime import datetime
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Mantém compatibilidade com routers/pedidos.py,
# que importa "pratos" deste arquivo.
pratos = []

DATABASE_URL = os.getenv("DATABASE_URL")


class PratoInput(BaseModel):
    nome: str
    categoria: str
    preco: float
    preco_promocional: Optional[float] = None
    descricao: Optional[str] = None
    disponivel: bool = True


def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL não configurada")

    last_error = None
    for _ in range(10):
        try:
            return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        except Exception as e:
            last_error = e
            time.sleep(1)

    raise last_error


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pratos (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco FLOAT NOT NULL,
            preco_promocional FLOAT NULL,
            descricao TEXT NULL,
            disponivel BOOLEAN NOT NULL DEFAULT TRUE,
            criado_em TIMESTAMP NOT NULL
        );
    """)

    cur.execute("SELECT COUNT(*) AS total FROM pratos;")
    total = cur.fetchone()["total"]

    if total == 0:
        cur.execute("""
            INSERT INTO pratos
            (nome, categoria, preco, preco_promocional, descricao, disponivel, criado_em)
            VALUES
            ('Pizza Portuguesa', 'pizza', 59.9, NULL, 'Pizza Clássica Portuguesa', TRUE, '2024-01-01T00:00:00'),
            ('Nhoque ao Sugo', 'massa', 44.9, NULL, 'Massa ao sugo', TRUE, '2024-01-01T00:00:00'),
            ('Pudim de Leite', 'sobremesa', 16.9, NULL, 'Sobremesa de pudim', TRUE, '2024-01-01T00:00:00');
        """)

    conn.commit()
    cur.close()
    conn.close()


@router.get("/")
def listar_pratos():
    init_db()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pratos ORDER BY id;")
    resultado = cur.fetchall()
    cur.close()
    conn.close()

    return resultado


@router.post("/")
def criar_prato(prato: PratoInput):
    init_db()

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO pratos
        (nome, categoria, preco, preco_promocional, descricao, disponivel, criado_em)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
        """,
        (
            prato.nome,
            prato.categoria,
            prato.preco,
            prato.preco_promocional,
            prato.descricao,
            prato.disponivel,
            datetime.now(),
        ),
    )

    novo_prato = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return novo_prato


@router.get("/{prato_id}")
def buscar_prato(prato_id: int):
    init_db()

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pratos WHERE id = %s;", (prato_id,))
    prato = cur.fetchone()
    cur.close()
    conn.close()

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    return prato
