import json

import pytest
from app.core.models import User
from app.perguntas.models import Pergunta, Alternativa, Tema
from app.graphql import eg, inputs
from graphene_django.utils.testing import graphql_query
from django.contrib.auth.models import Group
from model_bakery import baker



@pytest.mark.django_db
def test_deve_criar_nova_pergunta(client_with_login, user):
    tema = baker.make("Tema", _fill_optional=True)

    assert Pergunta.objects.exists() is False

    resultado = graphql_query(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables = {
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": False,
                "alternativas": [
                    {
                        "texto": "London",
                        "correta": False
                    },
                    {
                        "texto": "Berlin",
                        "correta": False
                    },
                    {
                        "texto": "Paris",
                        "correta": True
                    },
                    {
                        "texto": "Madrid",
                        "correta": False
                    }
                ]
            }
        },
        client=client_with_login
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
    assert pergunta_criada.alternativas_corretas.get() == Alternativa.objects.get(texto="Paris", correta=True)


# TODO
# Usuario deslogado não deve criar 
# Não deve criar pergunta ou alternativas caso qualquer um de erro
#   testar tema invalido
#   testar alternativa invalida
#   testar algum valor de pergunta invalido


@pytest.mark.django_db
def test_nao_deve_criar_nova_pergunta_se_for_usuario_anonimo(client_graphql_without_login):
    tema = baker.make("Tema", _fill_optional=True)

    assert Pergunta.objects.exists() is False

    resultado = client_graphql_without_login(
        query=eg.cadastrar_pergunta_mutation,
        operation_name="cadastrarPergunta",
        variables = {
            "novaPergunta": {
                "enunciado": "What is the capital of France?",
                "temaId": tema.id,
                "tipoResposta": inputs.TipoRespostaEnum.MES.name,
                "referencia": "Paris",
                "referenciaBiblica": False,
                "alternativas": [
                    {
                        "texto": "London",
                        "correta": False
                    },
                    {
                        "texto": "Berlin",
                        "correta": False
                    },
                    {
                        "texto": "Paris",
                        "correta": True
                    },
                    {
                        "texto": "Madrid",
                        "correta": False
                    }
                ]
            }
        },
    )

    assert "errors" in json.loads(resultado.content)

    assert Pergunta.objects.count() == 0
    assert Alternativa.objects.count() == 0