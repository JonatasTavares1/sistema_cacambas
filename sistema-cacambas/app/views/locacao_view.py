import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from ..database import SessionLocal
from ..models import Cliente, Cacamba, Aluguel

import os
from reportlab.pdfgen import canvas

def abrir_tela_locacao():
    janela = tk.Toplevel()
    janela.title("Nova Locação")
    janela.geometry("500x550")

    # ----- CAMPOS DO CLIENTE -----
    ttk.Label(janela, text="CPF/CNPJ do Cliente:").pack()
    entry_cpf = ttk.Entry(janela)
    entry_cpf.pack()

    ttk.Label(janela, text="Nome:").pack()
    entry_nome = ttk.Entry(janela)
    entry_nome.pack()

    ttk.Label(janela, text="Telefone:").pack()
    entry_telefone = ttk.Entry(janela)
    entry_telefone.pack()

    ttk.Label(janela, text="Endereço:").pack()
    entry_endereco = ttk.Entry(janela)
    entry_endereco.pack()

    def buscar_cliente():
        cpf = entry_cpf.get().strip()
        if not cpf:
            messagebox.showwarning("Aviso", "Informe o CPF/CNPJ para buscar.")
            return

        db = SessionLocal()
        cliente = db.query(Cliente).filter(Cliente.cpf_cnpj == cpf).first()
        db.close()

        if cliente:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, cliente.nome)
            entry_telefone.delete(0, tk.END)
            entry_telefone.insert(0, cliente.telefone)
            entry_endereco.delete(0, tk.END)
            entry_endereco.insert(0, cliente.endereco)
            messagebox.showinfo("Cliente encontrado", "Cliente preenchido automaticamente.")
        else:
            messagebox.showinfo("Não encontrado", "Cliente não encontrado. Preencha os dados abaixo.")

    ttk.Button(janela, text="🔍 Buscar Cliente", command=buscar_cliente).pack(pady=5)

    # ----- SELEÇÃO DE CAÇAMBAS -----
    db = SessionLocal()
    cacambas = db.query(Cacamba).filter_by(disponivel=True).all()
    db.close()

    ttk.Label(janela, text="Selecionar Caçamba:").pack()
    combo_cacamba = ttk.Combobox(janela, values=[f"{c.id} - {c.identificacao}" for c in cacambas])
    combo_cacamba.pack()

    ttk.Label(janela, text="Data de Devolução (dd/mm/aaaa):").pack()
    entry_data_fim = ttk.Entry(janela)
    entry_data_fim.pack()

    def gerar_recibo_pdf(cliente, aluguel, cacamba):
        recibo_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'recibos')
        os.makedirs(recibo_dir, exist_ok=True)

        nome_formatado = cliente.nome.strip().lower().replace(" ", "-")
        nome_arquivo = f"recibo_{nome_formatado}.pdf"
        caminho = os.path.join(recibo_dir, nome_arquivo)

        c = canvas.Canvas(caminho)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 800, "RECIBO DE LOCAÇÃO DE CAÇAMBA")

        c.setFont("Helvetica", 12)
        c.drawString(50, 760, f"Cliente: {cliente.nome}")
        c.drawString(50, 740, f"CPF/CNPJ: {cliente.cpf_cnpj}")
        c.drawString(50, 720, f"Telefone: {cliente.telefone}")
        c.drawString(50, 700, f"Endereço: {cliente.endereco}")
        c.drawString(50, 680, f"Caçamba: {cacamba.identificacao}")
        c.drawString(50, 660, f"Data de Início: {aluguel.data_inicio.strftime('%d/%m/%Y')}")
        c.drawString(50, 640, f"Data de Devolução: {aluguel.data_fim.strftime('%d/%m/%Y')}")
        c.drawString(50, 620, f"ID do Aluguel: {aluguel.id}")
        c.drawString(50, 580, "Assinatura: ____________________________")
        c.drawString(50, 560, "Data: ____/____/______")
        c.save()
        return caminho

    def confirmar_locacao():
        cpf = entry_cpf.get().strip()
        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()
        endereco = entry_endereco.get().strip()
        cacamba_id = combo_cacamba.get().split(" - ")[0] if combo_cacamba.get() else None
        data_fim_str = entry_data_fim.get().strip()

        if not (cpf and nome and telefone and endereco and cacamba_id and data_fim_str):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data de devolução inválida.")
            return

        try:
            db = SessionLocal()

            cliente = db.query(Cliente).filter(Cliente.cpf_cnpj == cpf).first()
            if not cliente:
                cliente = Cliente(nome=nome, cpf_cnpj=cpf, telefone=telefone, endereco=endereco)
                db.add(cliente)
                db.flush()

            aluguel = Aluguel(
                cliente_id=cliente.id,
                cacamba_id=int(cacamba_id),
                data_fim=data_fim,
                encerrado=False
            )
            db.add(aluguel)

            cacamba = db.query(Cacamba).filter_by(id=int(cacamba_id)).first()
            cacamba.disponivel = False

            db.commit()

            recibo_path = gerar_recibo_pdf(cliente, aluguel, cacamba)
            messagebox.showinfo("Sucesso", f"Locação registrada!\nRecibo salvo em:\n{recibo_path}")
            janela.destroy()
        except SQLAlchemyError as e:
            db.rollback()
            messagebox.showerror("Erro", f"Erro no banco de dados:\n{e}")
        finally:
            db.close()

    ttk.Button(janela, text="✅ Confirmar Aluguel", command=confirmar_locacao).pack(pady=20)
