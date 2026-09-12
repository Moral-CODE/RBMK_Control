import sqlite3
from datetime import datetime


def conectar():
    return sqlite3.connect("rbmk.db")


def criar_tabela():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora_teste TEXT,
            tempo_alvo REAL,
            tempo_jogador REAL,
            acertou INTEGER,
            cravado INTEGER
        )
    """)

    # =========================================================
    # ATUALIZAÇÃO DO BANCO
    # =========================================================

    cursor.execute("""
        PRAGMA table_info(partidas)
    """)

    colunas = [
        coluna[1]
        for coluna in cursor.fetchall()
    ]

    if "hora_teste" not in colunas:

        cursor.execute("""
            ALTER TABLE partidas
            ADD COLUMN hora_teste TEXT
        """)

    if "cravado" not in colunas:

        cursor.execute("""
            ALTER TABLE partidas
            ADD COLUMN cravado INTEGER DEFAULT 0
        """)

    conexao.commit()
    conexao.close()


def salvar_partida(
    tempo_alvo,
    tempo_jogador,
    acertou
):

    conexao = conectar()
    cursor = conexao.cursor()

    hora_teste = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cravado = (
        1
        if acertou and abs(
            tempo_jogador - tempo_alvo
        ) <= 0.03
        else 0
    )

    cursor.execute("""
        INSERT INTO partidas (
            hora_teste,
            tempo_alvo,
            tempo_jogador,
            acertou,
            cravado
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        hora_teste,
        tempo_alvo,
        tempo_jogador,
        int(acertou),
        cravado
    ))

    conexao.commit()
    conexao.close()