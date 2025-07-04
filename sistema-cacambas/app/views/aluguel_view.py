import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from sqlalchemy.orm import joinedload
from ..database import SessionLocal
from ..models import Cliente, Cacamba, Aluguel

def abrir_tela_aluguel():
    janela = tk.Toplevel()
    janela.title("Registrar Aluguel")
    janela.geometry("450x400")

    db = SessionLocal()

    # Busca clientes e caçambas disponíveis
    clientes = db.query(Cliente).all()
    cacambas = db.query(Cacamba).filter_by(disponivel=True).all()

    db.close()

    # Widgets
    ttk.Label(janela, text="Cliente:").pack()
    combo_cliente = ttk.Combobox(janela, values=[f"{c.id} - {c.nome}" for c in clientes])
    combo_cliente.pack()

    ttk.Label(janela, text="Caçamba:").pack()
    combo_cacamba = ttk.Combobox(janela, values=[f"{c.id} - {c.identificacao}" for c in cacambas])
    combo_cacamba.pack()

    ttk.Label(janela, text="Data de Fim (dd/mm/aaaa):").pack()
    entry_data_fim = ttk.Entry(janela)
    entry_data_fim.pack()

    def registrar_aluguel():
        try:
            cliente_id = int(combo_cliente.get().split(" - ")[0])
            cacamba_id = int(combo_cacamba.get().split(" - ")[0])
            data_fim_str = entry_data_fim.get()
            data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y")

            db = SessionLocal()

            novo_aluguel = Aluguel(
                cliente_id=cliente_id,
                cacamba_id=cacamba_id,
                data_fim=data_fim
            )
            db.add(novo_aluguel)

            # Marca a caçamba como indisponível
            cacamba = db.query(Cacamba).filter_by(id=cacamba_id).first()
            cacamba.disponivel = False

            db.commit()
            db.close()

            messagebox.showinfo("Sucesso", "Aluguel registrado!")
            janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar aluguel: {e}")

    ttk.Button(janela, text="Salvar Aluguel", command=registrar_aluguel).pack(pady=20)

def abrir_tela_devolucao():
    janela = tk.Toplevel()
    janela.title("Registrar Devolução")
    janela.geometry("500x400")

    db = SessionLocal()

    # Busca aluguéis ativos com join de cliente e caçamba
    alugueis = db.query(Aluguel).filter_by(encerrado=False)\
        .options(joinedload(Aluguel.cliente), joinedload(Aluguel.cacamba)).all()

    db.close()

    # Lista amigável para exibição
    lista_exibicao = []
    for a in alugueis:
        nome_cliente = a.cliente.nome
        id_cacamba = a.cacamba.identificacao
        fim = a.data_fim.strftime('%d/%m/%Y')
        lista_exibicao.append(f"{a.id} - {nome_cliente} - Caçamba {id_cacamba} - Devolução: {fim}")

    ttk.Label(janela, text="Selecione um aluguel para devolver:").pack()
    combo = ttk.Combobox(janela, values=lista_exibicao, width=60)
    combo.pack(pady=10)

    def confirmar_devolucao():
        try:
            aluguel_id = int(combo.get().split(" - ")[0])

            db = SessionLocal()
            aluguel = db.query(Aluguel).filter_by(id=aluguel_id).first()
            aluguel.encerrado = True

            caçamba = db.query(Cacamba).filter_by(id=aluguel.cacamba_id).first()
            caçamba.disponivel = True

            db.commit()
            db.close()

            messagebox.showinfo("Sucesso", "Devolução registrada com sucesso!")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar devolução: {e}")

    ttk.Button(janela, text="Registrar Devolução", command=confirmar_devolucao).pack(pady=20)