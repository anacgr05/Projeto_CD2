import sqlite3
import time
from datetime import datetime
from typing import Optional

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import APIRouter, HTTPException
from models.prato import PratoInput

from config import settings

router = APIRouter()

# Mantém compatibilidade com routers/pedidos.py,
# que importa "pratos" deste arquivo.
pratos = []

DATABASE_URL = settings.database_url
IS_SQLITE = DATABASE_URL.startswith("sqlite:///")
SQLITE_DB_PATH = DATABASE_URL[len("sqlite:///") :] if IS_SQLITE else None


def _format_query(query: str) -> str:
    return query.replace("%s", "?") if IS_SQLITE else query


def _row_to_dict(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    try:
        return dict(row)
    except Exception:
        return row


def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL não configurada")

    if IS_SQLITE:
        try:
            conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            raise RuntimeError(f"Erro ao conectar no SQLite: {e}") from e

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

    if IS_SQLITE:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                preco_promocional REAL NULL,
                descricao TEXT NULL,
                disponivel INTEGER NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL
            );
            """)
    else:
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

    cur.execute(_format_query("SELECT COUNT(*) AS total FROM pratos;"))
    total = cur.fetchone()[0] if IS_SQLITE else cur.fetchone()["total"]

    if total == 0:
        cur.execute(
            _format_query("""
                INSERT INTO pratos
                (nome, categoria, preco, preco_promocional, descricao, disponivel, criado_em)
                VALUES
                ('Pizza Portuguesa', 'pizza', 59.9, NULL, 'Pizza Clássica Portuguesa', %s, '2024-01-01T00:00:00'),
                ('Nhoque ao Sugo', 'massa', 44.9, NULL, 'Massa ao sugo', %s, '2024-01-01T00:00:00'),
                ('Pudim de Leite', 'sobremesa', 16.9, NULL, 'Sobremesa de pudim', %s, '2024-01-01T00:00:00');
                """),
            (
                1 if IS_SQLITE else True,
                1 if IS_SQLITE else True,
                1 if IS_SQLITE else True,
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


@router.get("/")
def listar_pratos(categoria: Optional[str] = None):
    init_db()

    conn = get_conn()
    cur = conn.cursor()

    if categoria:
        query = _format_query("SELECT * FROM pratos WHERE categoria = %s ORDER BY id;")
        params = (categoria,)
    else:
        query = _format_query("SELECT * FROM pratos ORDER BY id;")
        params = ()

    cur.execute(query, params)
    resultado = cur.fetchall()
    cur.close()
    conn.close()

    return [_row_to_dict(row) for row in resultado]


@router.post("/")
def criar_prato(prato: PratoInput):
    init_db()

    conn = get_conn()
    cur = conn.cursor()

    insert_query = _format_query("""
        INSERT INTO pratos
        (nome, categoria, preco, preco_promocional, descricao, disponivel, criado_em)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)

    insert_values = (
        prato.nome,
        prato.categoria,
        prato.preco,
        prato.preco_promocional,
        prato.descricao,
        1 if prato.disponivel else 0 if IS_SQLITE else prato.disponivel,
        datetime.now(),
    )

    cur.execute(insert_query, insert_values)

    if IS_SQLITE:
        prato_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        returned = None
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(_format_query("SELECT * FROM pratos WHERE id = ?;"), (prato_id,))
        returned = cur.fetchone()
        cur.close()
        conn.close()
        return _row_to_dict(returned)

    novo_prato = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return _row_to_dict(novo_prato)


@router.get("/{prato_id}")
def buscar_prato(prato_id: int):
    init_db()

    conn = get_conn()
    cur = conn.cursor()
    query = _format_query("SELECT * FROM pratos WHERE id = %s;")
    cur.execute(query, (prato_id,))
    prato = cur.fetchone()
    cur.close()
    conn.close()

    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    return _row_to_dict(prato)
