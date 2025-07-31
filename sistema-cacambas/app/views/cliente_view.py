# ═══════════════════════════════════════════════════════════════════════════════
# CADASTRO DE CLIENTE - INTERFACE MODERNA
# ═══════════════════════════════════════════════════════════════════════════════

import customtkinter as ctk
from tkinter import messagebox
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.models import Cliente


def construir_tela_cliente(pai: ctk.CTkFrame) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(pai, corner_radius=10)
    frame.grid_columnconfigure(0, weight=1)

    # ─── Título ─────────────────────────────────────────────────────────
    ctk.CTkLabel(
        frame,
        text="👤 Cadastro de Cliente",
        font=("Segoe UI", 22, "bold")
    ).grid(row=0, column=0, pady=(20, 10), sticky="n")

    # ─── Campo: Nome completo ───────────────────────────────────────────
    entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome completo", width=400)
    entry_nome.grid(row=1, column=0, pady=6)

    # ─── Campo: CPF ou CNPJ ─────────────────────────────────────────────
    entry_cpf_cnpj = ctk.CTkEntry(frame, placeholder_text="CPF ou CNPJ", width=400)
    entry_cpf_cnpj.grid(row=2, column=0, pady=6)

    # ─── Campo: E-mail ──────────────────────────────────────────────────
    entry_email = ctk.CTkEntry(frame, placeholder_text="E-mail", width=400)
    entry_email.grid(row=3, column=0, pady=6)

    # ─── Campo: Endereço ────────────────────────────────────────────────
    entry_endereco = ctk.CTkEntry(frame, placeholder_text="Endereço (rua, avenida etc.)", width=400)
    entry_endereco.grid(row=4, column=0, pady=6)

    # ─── Campo: Telefone ────────────────────────────────────────────────
    entry_telefone = ctk.CTkEntry(frame, placeholder_text="Telefone", width=400)
    entry_telefone.grid(row=5, column=0, pady=6)

    # ─── Botão de salvar ────────────────────────────────────────────────
    def salvar_cliente():
        nome = entry_nome.get().strip()
        cpf_cnpj = entry_cpf_cnpj.get().strip()
        email = entry_email.get().strip()
        endereco = entry_endereco.get().strip()
        telefone = entry_telefone.get().strip()

        if not nome or not cpf_cnpj:
            messagebox.showerror("Erro", "Nome e CPF/CNPJ são obrigatórios.")
            return

        try:
            with SessionLocal() as db:
                if db.query(Cliente).filter_by(cpf_cnpj=cpf_cnpj).first():
                    messagebox.showerror("Erro", "Já existe um cliente com este CPF/CNPJ.")
                    return

                novo = Cliente(
                    nome=nome,
                    cpf_cnpj=cpf_cnpj,
                    email=email,
                    endereco=endereco,
                    telefone=telefone
                )
                db.add(novo)
                db.commit()

            messagebox.showinfo("Sucesso", "✅ Cliente cadastrado com sucesso!")

            entry_nome.delete(0, "end")
            entry_cpf_cnpj.delete(0, "end")
            entry_email.delete(0, "end")
            entry_endereco.delete(0, "end")
            entry_telefone.delete(0, "end")

        except SQLAlchemyError as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco:\n{e}")

    ctk.CTkButton(
        frame,
        text="💾 Salvar Cliente",
        command=salvar_cliente,
        width=250,
        height=40,
        font=("Segoe UI", 14, "bold")
    ).grid(row=6, column=0, pady=20)

    return frame
