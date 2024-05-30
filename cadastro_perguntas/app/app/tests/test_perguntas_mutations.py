import json

import pytest
from app.perguntas.models import Pergunta, Alternativa, Tema
from app.graphql import eg, inputs
from graphene_django.utils.testing import graphql_query
from model_bakery import baker


@pytest.mark.django_db
def test_deve_criar_nova_pergunta(client_with_login, user):
    tema = baker.make("Tema", _fill_optional=True)

    assert Pergunta.objects.exists() is False

    resultado = graphql_query(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables={
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": False,
                "alternativas": [
                    {"texto": "London", "correta": False},
                    {"texto": "Berlin", "correta": False},
                    {"texto": "Paris", "correta": True},
                    {"texto": "Madrid", "correta": False},
                ],
            }
        },
        client=client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta_criada = Pergunta.objects.get()
    assert Pergunta.objects.count() == 1
    assert Alternativa.objects.count() == 4
    assert Alternativa.objects.filter(texto="London").exists() is True
    assert Alternativa.objects.filter(texto="Berlin").exists() is True
    assert Alternativa.objects.filter(texto="Paris").exists() is True
    assert Alternativa.objects.filter(texto="Madrid").exists() is True

    assert pergunta_criada.enunciado == "What is the capital of France?"
    assert pergunta_criada.tipo_resposta == "MES"
    assert pergunta_criada.referencia == "Paris"
    assert pergunta_criada.referencia_biblica is False
    assert pergunta_criada.criado_por == user
    assert pergunta_criada.tema == tema
    assert pergunta_criada.alternativas_corretas.count() == 1
    assert pergunta_criada.alternativas_corretas.get() == Alternativa.objects.get(
        texto="Paris", correta=True
    )


@pytest.mark.django_db
def test_nao_deve_criar_nova_pergunta_se_for_usuario_anonimo(
    client_graphql_without_login,
):
    tema = baker.make("Tema", _fill_optional=True)

    assert Pergunta.objects.exists() is False

    resultado = client_graphql_without_login(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables={
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": False,
                "alternativas": [
                    {"texto": "London", "correta": False},
                    {"texto": "Berlin", "correta": False},
                    {"texto": "Paris", "correta": True},
                    {"texto": "Madrid", "correta": False},
                ],
            }
        },
    )

    assert "errors" in json.loads(resultado.content)

    assert Pergunta.objects.count() == 0
    assert Alternativa.objects.count() == 0


@pytest.mark.django_db
def test_nao_deve_criar_nova_pergunta_se_nao_enviar_um_tema_valido(client_with_login):
    assert Pergunta.objects.exists() is False

    resultado = graphql_query(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables={
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": 1,  # Give a invalid teme
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": False,
                "alternativas": [
                    {"texto": "London", "correta": False},
                    {"texto": "Berlin", "correta": False},
                    {"texto": "Paris", "correta": True},
                    {"texto": "Madrid", "correta": False},
                ],
            }
        },
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    assert Pergunta.objects.count() == 0
    assert Alternativa.objects.count() == 0


@pytest.mark.django_db
def test_nao_deve_criar_nova_pergunta_se_nao_enviar_uma_pergunta_valida(
    client_with_login,
):
    tema = baker.make("Tema", _fill_optional=True)
    assert Pergunta.objects.exists() is False

    resultado = graphql_query(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables={
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": "INVALIDO",
                "referencia": "Paris",
                "referenciaBiblica": False,
                "alternativas": [
                    {"texto": "London", "correta": False},
                    {"texto": "Berlin", "correta": False},
                    {"texto": "Paris", "correta": True},
                    {"texto": "Madrid", "correta": False},
                ],
            }
        },
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    assert Pergunta.objects.count() == 0
    assert Alternativa.objects.count() == 0


@pytest.mark.django_db
def test_nao_deve_criar_nova_pergunta_se_nao_enviar_uma_alternativa_valida(
    client_with_login,
):
    tema = baker.make("Tema", _fill_optional=True)
    assert Pergunta.objects.exists() is False

    resultado = graphql_query(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables={
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": False,
                "alternativas": [
                    {"texto": "London", "correta": "False"},
                    {"texto": "Berlin", "correta": False},
                    {"texto": "Paris", "correta": True},
                    {"texto": "Madrid", "correta": False},
                ],
            }
        },
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    assert Pergunta.objects.count() == 0
    assert Alternativa.objects.count() == 0


@pytest.mark.django_db
def test_deve_criar_nova_pergunta_com_referencia_biblica(
    client_with_login, user, mocker_request_get
):
    tema = baker.make("Tema", _fill_optional=True)

    assert Pergunta.objects.exists() is False
    assert mocker_request_get.called is False

    resultado = graphql_query(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables={
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": True,
                "alternativas": [
                    {"texto": "London", "correta": False},
                    {"texto": "Berlin", "correta": False},
                    {"texto": "Paris", "correta": True},
                    {"texto": "Madrid", "correta": False},
                ],
            }
        },
        client=client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta_criada = Pergunta.objects.get()
    assert Pergunta.objects.count() == 1
    assert Alternativa.objects.count() == 4
    assert pergunta_criada.referencia == "Paris"
    assert pergunta_criada.referencia_biblica is True
    assert mocker_request_get.called is True


@pytest.mark.django_db
def test_nao_deve_criar_nova_pergunta_com_referencia_biblica_caso_invalida(
    client_with_login, user, mocker_request_get_error
):
    tema = baker.make("Tema", _fill_optional=True)

    assert Pergunta.objects.exists() is False
    assert mocker_request_get_error.called is False

    resultado = graphql_query(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables={
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": True,
                "alternativas": [
                    {"texto": "London", "correta": False},
                    {"texto": "Berlin", "correta": False},
                    {"texto": "Paris", "correta": True},
                    {"texto": "Madrid", "correta": False},
                ],
            }
        },
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    assert Pergunta.objects.count() == 0
    assert Alternativa.objects.count() == 0
    assert mocker_request_get_error.called is True


@pytest.mark.django_db
def test_deve_criar_novo_tema(client_with_login):
    assert Tema.objects.exists() is False

    resultado = graphql_query(
        query=eg.cadastrar_tema_mutation,
        operation_name="cadastrarTema",
        variables={
            "novoTema": {
                "nome": "nomeTema",
                "cor": "vermel",
            }
        },
        client=client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    tema_criado = Tema.objects.get()
    assert Tema.objects.count() == 1
    assert tema_criado.nome == "nomeTema"
    assert tema_criado.cor == "vermel"


@pytest.mark.django_db
def test_nao_deve_criar_novo_tema_se_for_usuario_anonimo(client):
    assert Tema.objects.exists() is False

    resultado = graphql_query(
        query=eg.cadastrar_tema_mutation,
        operation_name="cadastrarTema",
        variables={
            "novoTema": {
                "nome": "nomeTema",
                "cor": "vermel",
            }
        },
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    assert Tema.objects.exists() is False


@pytest.mark.django_db
def test_deve_deletar_tema(admin_client_with_login):
    tema = baker.make("Tema", _fill_optional=True)
    assert Tema.objects.exists() is True

    resultado = graphql_query(
        query=eg.deletar_tema_mutation,
        operation_name="deletarTema",
        variables={"temaId": tema.id},
        client=admin_client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    assert Tema.objects.exists() is False
    assert (
        resultado.json()["data"]["deletarTema"]["mensagem"]
        == f"Tema #{tema.id} deletado com sucesso"
    )


@pytest.mark.django_db
def test_nao_deve_deletar_tema_se_usuario_nao_for_admin(client_with_login):
    tema = baker.make("Tema", _fill_optional=True)
    assert Tema.objects.exists() is True

    resultado = graphql_query(
        query=eg.deletar_tema_mutation,
        operation_name="deletarTema",
        variables={"temaId": tema.id},
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    assert Tema.objects.exists() is True


@pytest.mark.django_db
def test_nao_deve_deletar_tema_se_usuario_for_anonimo(client):
    tema = baker.make("Tema", _fill_optional=True)
    assert Tema.objects.exists() is True

    resultado = graphql_query(
        query=eg.deletar_tema_mutation,
        operation_name="deletarTema",
        variables={"temaId": tema.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    assert Tema.objects.exists() is True
