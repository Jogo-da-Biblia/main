import json

import pytest
from app.comentarios.models import Comentario
from app.graphql import eg
from graphene_django.utils.testing import graphql_query
from model_bakery import baker
from freezegun import freeze_time


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_deve_criar_novo_comentario(client_with_login, user):
    pergunta = baker.make("Pergunta")

    assert Comentario.objects.exists() is False

    resultado = graphql_query(
        query=eg.adicionar_comentario_mutation,
        operation_name="adicionarComentario",
        variables={
            "mensagem": "mensagem",
            "perguntaId": pergunta.id,
            "phone": "12345678911",
            "isWhatsapp": False,
        },
        client=client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    assert Comentario.objects.count() == 1
    comentario_criado = Comentario.objects.get()
    assert comentario_criado.mensagem == "mensagem"
    assert comentario_criado.pergunta == pergunta
    assert comentario_criado.phone == "12345678911"
    assert comentario_criado.is_whatsapp is False
    assert comentario_criado.email == user.email
    assert comentario_criado.criado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.comentarios.first() == comentario_criado


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_usuario_anonimo_deve_criar_novo_comentario(client):
    pergunta = baker.make("Pergunta")

    assert Comentario.objects.exists() is False

    resultado = graphql_query(
        query=eg.adicionar_comentario_mutation,
        operation_name="adicionarComentario",
        variables={
            "mensagem": "mensagem",
            "email": "email@teste.com",
            "perguntaId": pergunta.id,
            "phone": "12345678911",
        },
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    assert Comentario.objects.count() == 1
    comentario_criado = Comentario.objects.get()
    assert comentario_criado.mensagem == "mensagem"
    assert comentario_criado.pergunta == pergunta
    assert comentario_criado.phone == "12345678911"
    assert comentario_criado.is_whatsapp is True
    assert comentario_criado.email == "email@teste.com"
    assert comentario_criado.criado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.comentarios.first() == comentario_criado


@pytest.mark.parametrize(
    ("invalid_email"),
    ["  ", None],
)
@pytest.mark.django_db
def test_usuario_anonimo_nao_deve_criar_novo_comentario_sem_email(
    client, invalid_email
):
    pergunta = baker.make("Pergunta")

    assert Comentario.objects.exists() is False

    resultado = graphql_query(
        query=eg.adicionar_comentario_mutation,
        operation_name="adicionarComentario",
        variables={
            "mensagem": "mensagem",
            "email": invalid_email,
            "perguntaId": pergunta.id,
            "phone": "12345678911",
        },
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    assert Comentario.objects.count() == 0


@pytest.mark.parametrize(
    ("invalid_message"),
    ["  ", None],
)
@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_nao_deve_criar_novo_comentario_se_mensagem_for_vazia(
    client_with_login, invalid_message
):
    pergunta = baker.make("Pergunta")

    assert Comentario.objects.exists() is False

    resultado = graphql_query(
        query=eg.adicionar_comentario_mutation,
        operation_name="adicionarComentario",
        variables={
            "mensagem": invalid_message,
            "perguntaId": pergunta.id,
            "phone": "12345678911",
            "isWhatsapp": False,
        },
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    assert Comentario.objects.count() == 0


@pytest.mark.parametrize(
    ("invalid_message"),
    ["  ", None],
)
@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_usuario_anonimo_nao_deve_criar_novo_comentario_se_mensagem_for_vazia(
    client, invalid_message
):
    pergunta = baker.make("Pergunta")

    assert Comentario.objects.exists() is False

    resultado = graphql_query(
        query=eg.adicionar_comentario_mutation,
        operation_name="adicionarComentario",
        variables={
            "mensagem": invalid_message,
            "perguntaId": pergunta.id,
            "phone": "12345678911",
            "isWhatsapp": False,
        },
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    assert Comentario.objects.count() == 0
