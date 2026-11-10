from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "salao_luh_2026"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "banco.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                telefone TEXT NOT NULL,
                data TEXT NOT NULL,
                horario TEXT NOT NULL,
                servico TEXT NOT NULL
            )
        """)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/agendar", methods=["POST"])
def agendar():

    cliente = request.form.get("cliente", "").strip()
    telefone = request.form.get("telefone", "").strip()
    data = request.form.get("data", "")
    horario = request.form.get("horario", "")
    servico = request.form.get("servico", "")

    if not all([cliente, telefone, data, horario, servico]):
        flash("Preencha todos os campos.")
        return redirect(url_for("inicio"))

    with conectar() as conn:
        conn.execute("""
            INSERT INTO agendamentos
            (cliente, telefone, data, horario, servico)
            VALUES (?, ?, ?, ?, ?)
        """, (cliente, telefone, data, horario, servico))

    flash("Agendamento realizado com sucesso!")

    return redirect(url_for("inicio"))


@app.route("/agendamentos")
def agendamentos():

    with conectar() as conn:
        registros = conn.execute("""
            SELECT * FROM agendamentos
            ORDER BY data, horario
        """).fetchall()

    return render_template(
        "agendamentos.html",
        registros=registros
    )


@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):

    with conectar() as conn:
        conn.execute(
            "DELETE FROM agendamentos WHERE id = ?",
            (id,)
        )

    flash("Agendamento excluído com sucesso!")

    return redirect(url_for("agendamentos"))


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)