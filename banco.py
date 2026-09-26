import sqlite3
import pandas as pd

NOME_BANCO = "academia.db"

def conectar():
    return sqlite3.connect(NOME_BANCO)

def criar_tabela():
    conexao = conectar()
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            modalidade TEXT NOT NULL,
            instrutor TEXT NOT NULL,
            valor_mensalidade REAL NOT NULL,
            data_checkin TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()

def inserir_checkin(aluno, modalidade, instrutor, valor_mensalidade, data_checkin):
    conexao = conectar()
    conexao.execute(
        """
        INSERT INTO checkins (aluno, modalidade, instrutor, valor_mensalidade, data_checkin)
        VALUES (?, ?, ?, ?, ?)
        """,
        (aluno, modalidade, instrutor, valor_mensalidade, data_checkin)
    )
    conexao.commit()
    conexao.close()

def listar_checkins():
    conexao = conectar()
    df = pd.read_sql_query("SELECT * FROM checkins ORDER BY id DESC", conexao)
    conexao.close()
    return df

def excluir_checkin(id_checkin):
    conexao = conectar()
    conexao.execute("DELETE FROM checkins WHERE id = ?", (id_checkin,))
    conexao.commit()
    conexao.close()