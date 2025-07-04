import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from ..database import SessionLocal
from ..models import Cliente

def abrir_tela_cliente():
    janela = tk.Toplevel()
    janela.title("Cadastro de Cliente")
    janela.geometry("400x300")

    # Campos
    ttk.Label(janela, text="Nome:").pack()
    entry_nome = ttk.Entry(janela)
    entry_nome.pack()

    ttk.Label(janela, text="Telefone:").pack()
    entry_telefone = ttk.Entry(janela)
    entry_telefone.pack()

    ttk.Label(janela, text="Endereço:").pack()
    entry_endereco = ttk.Entry(janela)
    entry_endereco.pack()

    def salvar_cliente():
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        endereco = entry_endereco.get()

        if not nome.strip():
            messagebox.showerror("Erro", "O nome é obrigatório.")
            return

        try:
            db = SessionLocal()
            novo_cliente = Cliente(nome=nome, telefone=telefone, endereco=endereco)
            db.add(novo_cliente)
            db.commit()
            db.close()
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            janela.destroy()
        except SQLAlchemyError as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

    ttk.Button(janela, text="Salvar", command=salvar_cliente).pack(pady=10)