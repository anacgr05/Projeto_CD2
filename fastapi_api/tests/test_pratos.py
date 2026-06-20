import pytest


@pytest.mark.smoke
def test_raiz_retorna_nome_restaurante(client):
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "restaurante" in body
    assert body["restaurante"] == "Bella Tavola"


@pytest.mark.smoke
def test_listar_pratos_retorna_200(client):
    response = client.get("/pratos")
    assert response.status_code == 200


@pytest.mark.smoke
def test_listar_pratos_retorna_lista(client):
    response = client.get("/pratos")
    assert isinstance(response.json(), list)


@pytest.mark.smoke
def test_lista_retorna_pratos_com_estrutura_correta(client):
    response = client.get("/pratos")
    assert response.status_code == 200
    pratos = response.json()
    assert len(pratos) > 0
    assert "id" in pratos[0]
    assert "nome" in pratos[0]
    assert "preco" in pratos[0]


@pytest.mark.smoke
def test_filtro_categoria_pizza_retorna_apenas_pizzas(client):
    response = client.get("/pratos?categoria=pizza")
    assert response.status_code == 200
    pratos = response.json()
    for prato in pratos:
        assert prato["categoria"] == "pizza"


@pytest.mark.smoke
def test_buscar_prato_existente_retorna_campos_esperados(client):
    response = client.get("/pratos/1")
    assert response.status_code == 200
    prato = response.json()
    assert "id" in prato
    assert "nome" in prato
    assert "preco" in prato


@pytest.mark.validacao
def test_buscar_prato_inexistente_retorna_404(client):
    response = client.get("/pratos/9999")
    assert response.status_code == 404


@pytest.mark.smoke
def test_criar_prato_valido(client):
    novo_prato = {
        "nome": "Funghi Trifolati Teste",
        "categoria": "massa",
        "preco": 49.9,
        "descricao": "Prato criado durante o teste",
        "disponivel": True,
    }
    response = client.post("/pratos", json=novo_prato)
    assert response.status_code in [200, 201]
    body = response.json()
    assert body["nome"] == novo_prato["nome"]
    assert body["categoria"] == novo_prato["categoria"]
    assert body["preco"] == novo_prato["preco"]
    assert "id" in body


@pytest.mark.validacao
@pytest.mark.parametrize(
    "categoria_invalida",
    [
        "esoterico",
        "fastfood",
        "japonesa",
        "PIZZA",
        "massa extra",
    ],
)
def test_categoria_invalida_retorna_422(client, categoria_invalida):
    prato = {"nome": "Prato Teste", "categoria": categoria_invalida, "preco": 40.0}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
@pytest.mark.parametrize("preco_invalido", [-1.0, -0.01, -100.0])
def test_preco_invalido_retorna_422(client, preco_invalido):
    prato = {"nome": "Prato Teste", "categoria": "pizza", "preco": preco_invalido}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
def test_nome_curto_retorna_422(client):
    prato = {"nome": "AB", "categoria": "pizza", "preco": 30.0}
    response = client.post("/pratos", json=prato)
    assert response.status_code == 422


@pytest.mark.validacao
@pytest.mark.parametrize("id_inexistente", [9999, 123456, 99999])
def test_prato_inexistente_retorna_404(client, id_inexistente):
    response = client.get(f"/pratos/{id_inexistente}")
    assert response.status_code == 404
