import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from .database import init_db, SessionLocal
from .views.cliente_view import abrir_tela_cliente
from .views.cacamba_view import abrir_tela_cacamba
from .views.aluguel_view import abrir_tela_aluguel, abrir_tela_devolucao
from .views.locacao_view import abrir_tela_locacao
from .models import Cacamba, Aluguel

def mostrar_dashboard(frame, root):
    for widget in frame.winfo_children():
        widget.destroy()

    db = SessionLocal()

    total_disponiveis = db.query(Cacamba).filter_by(disponivel=True).count()
    total_alugadas = db.query(Cacamba).filter_by(disponivel=False).count()

    hoje = datetime.today()
    limite = hoje + timedelta(days=2)

    vencendo = db.query(Aluguel).filter(
        Aluguel.encerrado == False,
        Aluguel.data_fim <= limite
    ).count()

    db.close()

    ttk.Label(frame, text="📊 Dashboard", font=("Helvetica", 16)).pack(pady=10)

    ttk.Label(frame, text=f"🚛 Caçambas Alugadas: {total_alugadas}", font=("Helvetica", 12)).pack(pady=5)
    ttk.Label(frame, text=f"✅ Caçambas Disponíveis: {total_disponiveis}", font=("Helvetica", 12)).pack(pady=5)
    ttk.Label(frame, text=f"⚠️ Caçambas vencendo em até 2 dias: {vencendo}", font=("Helvetica", 12), foreground="red").pack(pady=5)

    # Agora root é passado como argumento
    ttk.Button(root, text="📝 Nova Locação", command=abrir_tela_locacao).pack(pady=10)

def main():
    init_db()

    root = tk.Tk()
    root.title("Sistema de Caçambas - Menu Principal")
    root.geometry("400x450")

    dashboard_frame = ttk.Frame(root)
    dashboard_frame.pack(pady=20)

    # Passa root para a função
    mostrar_dashboard(dashboard_frame, root)

    ttk.Button(root, text="🔄 Atualizar Dashboard", command=lambda: mostrar_dashboard(dashboard_frame, root)).pack(pady=5)
    ttk.Button(root, text="📋 Clientes", command=abrir_tela_cliente).pack(pady=5)
    ttk.Button(root, text="🚛 Caçambas", command=abrir_tela_cacamba).pack(pady=5)
    ttk.Button(root, text="📆 Aluguéis", command=abrir_tela_aluguel).pack(pady=5)
    ttk.Button(root, text="↩️ Devoluções", command=abrir_tela_devolucao).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()