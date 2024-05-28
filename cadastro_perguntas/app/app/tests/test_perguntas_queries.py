import json

import pytest
from app.core.models import User
from app.graphql import eg
from graphene_django.utils.testing import graphql_query
from django.contrib.auth.models import Group
from model_bakery import baker


@pytest.mark.django_db
def test_deve_listar_todas_perguntas(client_with_login):
    baker.make("Pergunta", _fill_optional=True, _quantity=12)

    resultado = graphql_query(query=eg.todas_perguntas_query, client=client_with_login)

    assert "errors" not in json.loads(resultado.content)

    assert len(json.loads(resultado.content)["data"]["perguntas"]) == 12


@pytest.mark.django_db
def test_nao_deve_listar_todas_perguntas_caso_o_usuario_seja_anonimo(client):
    baker.make("Pergunta", _fill_optional=True, _quantity=12)

    resultado = graphql_query(query=eg.todas_perguntas_query, client=client)

    assert "errors" in json.loads(resultado.content)


@pytest.mark.django_db
def test_deve_listar_todas_perguntas_e_suas_informações(client_with_login):
    user = baker.make("core.User")
    tema = baker.make("Tema", _fill_optional=True)

    pergunta = baker.make("Pergunta", criado_por=user, tema=tema)

    alternativa_errada = baker.make("Alternativa", pergunta=pergunta, correta=False)
    alternativa_correta = baker.make("Alternativa", pergunta=pergunta, correta=True)

    comentario = baker.make("Comentario", pergunta=pergunta, _fill_optional=True)

    resultado = graphql_query(query=eg.todas_perguntas_query, client=client_with_login)

    assert "errors" not in json.loads(resultado.content)

    resultado_json = json.loads(resultado.content)["data"]["perguntas"][0]
    assert str(pergunta.id) == resultado_json["id"]
    assert pergunta.enunciado == resultado_json["enunciado"]
    assert pergunta.tipo_resposta == resultado_json["tipoResposta"]
    assert pergunta.referencia == resultado_json["referencia"]
    assert pergunta.status == resultado_json["status"]
    assert pergunta.criado_em.isoformat() == resultado_json["criadoEm"]
    assert pergunta.revisado_por == resultado_json["revisadoPor"]
    assert pergunta.revisado_status == resultado_json["revisadoStatus"]
    assert pergunta.revisado_em == resultado_json["revisadoEm"]
    assert pergunta.recusado_por == resultado_json["recusadoPor"]
    assert pergunta.publicado_por == resultado_json["publicadoPor"]
    assert pergunta.publicado_em == resultado_json["publicadoEm"]
    assert pergunta.atualizado_em.isoformat() == resultado_json["atualizadoEm"]

    assert str(tema.id) == resultado_json["tema"]["id"]
    assert tema.nome == resultado_json["tema"]["nome"]

    assert str(user.id) == resultado_json["criadoPor"]["id"]
    assert user.email == resultado_json["criadoPor"]["email"]

    assert len(resultado_json["alternativas"]) == 2
    assert f"'id': '{alternativa_correta.id}'" in str(resultado_json["alternativas"])
    assert f"'id': '{alternativa_errada.id}'" in str(resultado_json["alternativas"])

    assert len(resultado_json["alternativasCorretas"]) == 1
    assert (
        str(alternativa_correta.id) == resultado_json["alternativasCorretas"][0]["id"]
    )
    assert (
        alternativa_correta.texto == resultado_json["alternativasCorretas"][0]["texto"]
    )
    assert (
        alternativa_correta.correta
        == resultado_json["alternativasCorretas"][0]["correta"]
    )

    assert len(resultado_json["alternativasCorretas"]) == 1
    assert (
        str(alternativa_correta.id) == resultado_json["alternativasCorretas"][0]["id"]
    )
    assert (
        alternativa_correta.texto == resultado_json["alternativasCorretas"][0]["texto"]
    )
    assert (
        alternativa_correta.correta
        == resultado_json["alternativasCorretas"][0]["correta"]
    )

    assert len(resultado_json["comentarios"]) == 1
    assert str(comentario.id) == resultado_json["comentarios"][0]["id"]
    assert comentario.email == resultado_json["comentarios"][0]["email"]
    assert comentario.phone == resultado_json["comentarios"][0]["phone"]
    assert comentario.is_whatsapp == resultado_json["comentarios"][0]["isWhatsapp"]
    assert comentario.mensagem == resultado_json["comentarios"][0]["mensagem"]


@pytest.mark.django_db
def test_deve_listar_todas_os_temas(client_with_login):
    tema = baker.make("Tema", _fill_optional=True, _quantity=10)

    resultado = graphql_query(query=eg.todos_temas_query, client=client_with_login)

    assert "errors" not in json.loads(resultado.content)

    assert len(json.loads(resultado.content)["data"]["temas"]) == 10


@pytest.mark.django_db
def test_nao_deve_listar_todos_temas_caso_o_usuario_seja_anonimo(client):
    tema = baker.make("Tema", _fill_optional=True, _quantity=10)

    resultado = graphql_query(query=eg.todas_perguntas_query, client=client)

    assert "errors" in json.loads(resultado.content)


@pytest.mark.django_db
def test_deve_listar_todos_temas_e_suas_informações(client_with_login):
    tema = baker.make("Tema", _fill_optional=True)

    resultado = graphql_query(query=eg.todos_temas_query, client=client_with_login)

    assert "errors" not in json.loads(resultado.content)

    resultado_json = json.loads(resultado.content)["data"]["temas"][0]
    assert str(tema.id) == resultado_json["id"]
    assert tema.nome == resultado_json["nome"]
    assert tema.cor == resultado_json["cor"]
