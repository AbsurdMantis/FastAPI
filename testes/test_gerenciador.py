from fastapi.testclient import TestClient
from fastapi import status
from gerenciador_tarefas.gerenciador import app, TAREFAS


def test_quando_listar_tarefas_devo_ter_como_retorno_codigo_de_status_200():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.status_code == status.HTTP_200_OK
    

def test_quando_listar_tarefas_formato_de_retorno_deve_ser_json():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert resposta.headers["Content-Type"] == "application/json"


def test_quando_listar_tarefas_retorno_deve_ser_uma_lista():
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert isinstance(resposta.json(), list)


def test_titulo_da_tarefa_deve_conter_entre_3_e_50_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": 2 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    resposta = cliente.post("/tarefas", json={"titulo": 51 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_quando_uma_tarefa_e_submetida_deve_possuir_uma_descricao():
    cliente = TestClient(app)
    resposta = cliente.post("/tarefas", json={"titulo": "titulo"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_descricao_da_tarefa_pode_conter_no_maximo_140_caracteres():
    cliente = TestClient(app)
    resposta = cliente.post('/tarefas', json={"titulo" : "titulo", "descricao" : 141 * "*"})
    assert resposta.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# def test_quando_criar_uma_tarefa_a_mesma_deve_ser_retornada():
#     cliente = TestClient(app)
#     tarefa_esperada = {"titulo": "titulo", "descricao": "descricao"}
#     resposta = cliente.post("/tarefas", json=tarefa_esperada)
#     tarefa_criada = resposta.json()
#     assert tarefa_criada['titulo'] == tarefa_esperada['titulo']
#     assert tarefa_criada["descricao"] == tarefa_esperada["descricao"]
#     TAREFAS.clear()


# def test_quando_criar_uma_tarefa_seu_id_deve_ser_unico():
#     cliente = TestClient(app)
#     tarefa1 = {"titulo": "titulo1", "descricao": "descricao1"}
#     tarefa2 = {"titulo": "titulo2", "descricao": "descricao1"}
#     resposta1 = cliente.post("/tarefas", json=tarefa1)
#     resposta2 = cliente.post("/tarefas", json=tarefa2)
#     assert resposta1.json()["id"] != resposta2.json()["id"]
#     TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_id():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "id" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_titulo():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "titulo" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_descricao():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "descricao" in resposta.json().pop()
    TAREFAS.clear()


def test_quando_listar_tarefas_a_tarefa_retornada_deve_possuir_um_estado():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    assert "estado" in resposta.json().pop()
    TAREFAS.clear()

def test_quando_tarefa_não_finalizada():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "não finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.get("/tarefas")
    json = resposta.json().pop()
    assert True if ('não finalizado' in json['estado']) else False
    TAREFAS.clear()

def test_remover_tarefa():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "não finalizado",
        }
    )
    cliente = TestClient(app)
    resposta = cliente.delete("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66afa6")
    json = resposta.json()
    assert json == {'detail': 'Method Not Allowed'}
    TAREFAS.clear()

def test_concluir_tarefa():
    TAREFAS.append(
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "titulo": "titulo 1",
            "descricao": "descricao 1",
            "estado": "não finalizado",
        }
    )
    cliente = TestClient(app)
    # finalizado = {"estado" : "finalizado"}
    tarefa_especifica =  cliente.get("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66afa6")
    detalhes = tarefa_especifica.json()
    detalhes['estado'] = 'finalizado'
    resposta = cliente.put("/tarefas/3fa85f64-5717-4562-b3fc-2c963f66afa6", json=detalhes)
    #editar resposta
    atualizado = resposta.json()
    assert atualizado["estado"] == "finalizado"
    TAREFAS.clear()
