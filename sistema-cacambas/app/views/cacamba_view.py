import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.exc import SQLAlchemyError
from ..database import SessionLocal
from ..models import Cacamba

def abrir_tela_cacamba():
    janela = tk.Toplevel()
    janela.title("Gerenciar Caçambas")
    janela.geometry("400x300")

    # Campos
    ttk.Label(janela, text="Identificação:").pack()
    entry_id = ttk.Entry(janela)
    entry_id.pack()

    ttk.Label(janela, text="Localização atual:").pack()
    entry_local = ttk.Entry(janela)
    entry_local.pack()

    var_disponivel = tk.BooleanVar(value=True)
    chk_disponivel = ttk.Checkbutton(janela, text="Disponível", variable=var_disponivel)
    chk_disponivel.pack(pady=5)

    def salvar_cacamba():
        identificacao = entry_id.get()
        localizacao = entry_local.get()
        disponivel = var_disponivel.get()

        if not identificacao.strip():
            messagebox.showerror("Erro", "A identificação é obrigatória.")
            return

        try:
            db = SessionLocal()
            nova = Cacamba(
                identificacao=identificacao,
                localizacao_atual=localizacao,
                disponivel=disponivel
            )
            db.add(nova)
            db.commit()
            db.close()
            messagebox.showinfo("Sucesso", "Caçamba cadastrada com sucesso!")
            janela.destroy()
        except SQLAlchemyError as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

    ttk.Button(janela, text="Salvar", command=salvar_cacamba).pack(pady=10)