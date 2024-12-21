# Funções para criar, ler, atualizar e deletar tarefas.
from sqlmodel import Session, select
from app.models import Tarefa
from app.schemas import TarefaCreate, TarefaUpdate
from datetime import datetime

def criar_tarefa(db: Session, tarefa: TarefaCreate):
    db_tarefa = Tarefa(**tarefa.dict(), data_criacao=datetime.utcnow(), data_atualizacao=datetime.utcnow())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa

def listar_tarefas(db: Session):
    return db.exec(select(Tarefa)).all()

def obter_tarefa(db: Session, tarefa_id: int):
    return db.get(Tarefa, tarefa_id)

def atualizar_tarefa(db: Session, tarefa_id: int, tarefa: TarefaUpdate):
    db_tarefa = db.get(Tarefa, tarefa_id)
    if db_tarefa:
        for key, value in tarefa.dict(exclude_unset=True).items():
            setattr(db_tarefa, key, value)
        db_tarefa.data_atualizacao = datetime.utcnow()
        db.commit()
        db.refresh(db_tarefa)
        return db_tarefa
    return None

def deletar_tarefa(db: Session, tarefa_id: int):
    db_tarefa = db.get(Tarefa, tarefa_id)
    if db_tarefa:
        db.delete(db_tarefa)
        db.commit()
        return db_tarefa
    return None
