# Definições das tabelas e mapeamento com SQLModel.
from datetime import datetime
from sqlmodel import SQLModel, Field

class Tarefa(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # Remova autoincrement
    titulo: str
    descricao: str = None
    estado: str
    data_criacao: datetime = Field(default=datetime.utcnow)
    data_atualizacao: datetime = Field(default=datetime.utcnow, nullable=True)

