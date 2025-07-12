import json

import pytest
from app.graphql import eg
from graphene_django.utils.testing import graphql_query
from model_bakery import baker
from freezegun import freeze_time


@pytest.mark.django_db
def test_deve_listar_comentarios(client_with_login, client):
    comentario1 = baker.make("Comentario", _fill_optional=True)
    comentario2 = baker.make("Comentario", _fill_optional=True)

    clients_to_tests = [client_with_login, client]
    for current_client in clients_to_tests:
        resultado = graphql_query(
            query=eg.todos_comentarios_query, client=current_client
        )

        assert "errors" not in json.loads(resultado.content)

        assert {
            "id": str(comentario1.id),
            "mensagem": str(comentario1.mensagem),
            "email": str(comentario1.email),
            "phone": str(comentario1.phone),
            "pergunta": {
                "id": str(comentario1.pergunta.id),
                "enunciado": str(comentario1.pergunta.enunciado),
            },
        } in json.loads(resultado.content)["data"]["comentarios"]
        assert {
            "id": str(comentario2.id),
            "mensagem": str(comentario2.mensagem),
            "email": str(comentario2.email),
            "phone": str(comentario2.phone),
            "pergunta": {
                "id": str(comentario2.pergunta.id),
                "enunciado": str(comentario2.pergunta.enunciado),
            },
        } in json.loads(resultado.content)["data"]["comentarios"]
