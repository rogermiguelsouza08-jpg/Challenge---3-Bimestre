"""
Portal Web de Helpdesk — Script de criação do banco (Membro 1)
================================================================
Executa o schema.sql e cria o arquivo helpdesk.db (SQLite) com a
tabela "chamados" pronta para uso.

Rode este script UMA VEZ antes de usar a aplicação:
    python criar_banco.py
"""

import sqlite3
import os

DB_NAME = "helpdesk.db"
SCHEMA_FILE = "schema.sql"


def criar_banco():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as arquivo:
        cursor.executescript(arquivo.read())

    conn.commit()
    conn.close()
    print(f"Banco '{DB_NAME}' criado/atualizado com sucesso a partir de '{SCHEMA_FILE}'.")


if __name__ == "__main__":
    criar_banco()
