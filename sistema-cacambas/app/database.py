import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Caminho absoluto para a pasta raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(BASE_DIR, "sistema.db")  # <-- banco na raiz do projeto

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def init_db():
    from .models import Cliente, Cacamba, Aluguel
    Base.metadata.create_all(engine)