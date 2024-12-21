# Definição dos modelos Pydantic para validação de entrada e saída de dados.
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# Modelo para a criação de uma tarefa
class TarefaCreate(BaseModel):
    titulo: str = Field(..., description="Título da tarefa")
    descricao: Optional[str] = Field(None, description="Descrição da tarefa")
    estado: str = Field(..., description="Estado da tarefa")

# Modelo para a saída (listagem) de tarefas
class TarefaOut(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    estado: str
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True  # Configuração importante para converter objetos ORM em JSON

# Modelo para a atualização de tarefas
class TarefaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    estado: Optional[str] = None