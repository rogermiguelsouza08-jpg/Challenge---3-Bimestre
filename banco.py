"""
Portal Web de Helpdesk — Ponte entre o Banco (Membro 1) e a Interface (Membro 2)
=================================================================================
Este módulo é a "ponte": a interface gráfica (interface.py) nunca
conversa diretamente com o SQLite, ela apenas chama estas funções.
Isso mantém o trabalho do Membro 1 (banco) isolado do trabalho do
Membro 2 (tela), e qualquer um dos dois pode alterar sua parte sem
quebrar a do outro.
"""

import sqlite3
import pandas as pd

DB_NAME = "helpdesk.db"


def conectar():
    """Abre uma conexão com o arquivo do banco SQLite."""
    return sqlite3.connect(DB_NAME)


# ---------- CREATE ----------
def inserir_chamado(titulo: str, descricao: str, prioridade: str) -> None:
    """Insere um novo chamado. Status sempre inicia como 'Aberto'."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO chamados (titulo, descricao, prioridade, status)
        VALUES (?, ?, ?, ?)
        """,
        (titulo, descricao, prioridade, "Aberto"),
    )
    conn.commit()
    conn.close()


# ---------- READ ----------
def listar_chamados() -> pd.DataFrame:
    """Retorna todos os chamados como um DataFrame, pronto para a tabela."""
    conn = conectar()
    df = pd.read_sql_query("SELECT * FROM chamados ORDER BY id DESC", conn)
    conn.close()
    return df


# ---------- UPDATE ----------
def atualizar_status(chamado_id: int, novo_status: str) -> None:
    """Atualiza apenas o status de um chamado específico."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE chamados SET status = ? WHERE id = ?",
        (novo_status, chamado_id),
    )
    conn.commit()
    conn.close()


# ---------- DELETE ----------
def deletar_chamado(chamado_id: int) -> None:
    """Remove um chamado pelo id."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chamados WHERE id = ?", (chamado_id,))
    conn.commit()
    conn.close()
