import json
from uuid import UUID, uuid4
from fastapi import FastAPI
from pydantic import BaseModel, constr
from fastapi.encoders import jsonable_encoder

app = FastAPI()
class TarefaEntrada(BaseModel):
    titulo: constr(min_length=3, max_length=50)
    descrição: constr(max_length=140)
    estado: str
class Tarefa(TarefaEntrada):
    id: UUID

TAREFAS = [{
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "titulo": "fazer compras",
        "descrição": "comprar leite e ovos",
        "estado": "não finalizado",
    },
    {
        "id": "2",
        "titulo": "levar o cachorro para tosar",
        "descrição": "está muito peludo",
        "estado": "não finalizado",
    },
    {
        "id": "3",
        "titulo": "lavar roupas",
        "descrição": "estão sujas",
        "estado": "não finalizado",
    }]


@app.get("/tarefas")
def listar():
    return TAREFAS

@app.post('/tarefas', response_model=Tarefa)
def criar(tarefa: TarefaEntrada):
    nova_tarefa = tarefa.dict()
    nova_tarefa.update({"id": uuid4()})
    return nova_tarefa

@app.put("/tarefas/{id}", response_model=Tarefa)
def atualizar_estado(id: str, tarefa: Tarefa):
    atualizar_tarefa_encoded = jsonable_encoder(id)
    tarefa[id] = atualizar_tarefa_encoded
    return atualizar_tarefa_encoded
