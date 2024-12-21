# Arquivo principal para rodar a API FastAPI.
from sqlmodel import create_engine, SQLModel
from app.models import Tarefa

# Cria o banco de dados SQLite (se não existir)
DATABASE_URL = "sqlite:///./todolist.db"
engine = create_engine(DATABASE_URL, echo=True)

def criar_tabelas():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    criar_tabelas()


from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Tarefa
from app.schemas import TarefaCreate, TarefaOut, TarefaUpdate
from app.crud import criar_tarefa, listar_tarefas, obter_tarefa, atualizar_tarefa, deletar_tarefa
from sqlmodel import Session, create_engine

app = FastAPI()

# Conectar ao banco de dados
DATABASE_URL = "sqlite:///./todolist.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    with Session(engine) as session:
        yield session

@app.post("/tarefas/", response_model=TarefaOut, summary="Criar uma nova tarefa", description="Este endpoint cria uma nova tarefa no banco de dados.")
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = criar_tarefa(db, tarefa)
    return db_tarefa

@app.get("/tarefas/", response_model=list[TarefaOut])
def listar_tarefas_endpoint(db: Session = Depends(get_db)):
    return listar_tarefas(db)

@app.get("/tarefas/{tarefa_id}", response_model=TarefaOut)
def visualizar_tarefa_endpoint(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = obter_tarefa(db, tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.put("/tarefas/{tarefa_id}", response_model=TarefaOut)
def atualizar_tarefa_endpoint(tarefa_id: int, tarefa: TarefaUpdate, db: Session = Depends(get_db)):
    db_tarefa = atualizar_tarefa(db, tarefa_id, tarefa)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa

@app.delete("/tarefas/{tarefa_id}", response_model=TarefaOut)
def deletar_tarefa_endpoint(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = deletar_tarefa(db, tarefa_id)
    if db_tarefa is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_tarefa
