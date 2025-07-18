import json

import pytest
from app.perguntas.models import Pergunta, Alternativa, Tema
from app.graphql import eg, inputs
from graphene_django.utils.testing import graphql_query
from model_bakery import baker
from freezegun import freeze_time


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
def test_usuario_admin_deve_criar_nova_pergunta(admin_client_with_login, user):
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
        client=admin_client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    assert Pergunta.objects.count() == 1


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
def test_nao_deve_criar_nova_pergunta_se_usuario_nao_for_colaborador(
    client, publicador_user, revisor_user
):
    tema = baker.make("Tema", _fill_optional=True)

    assert Pergunta.objects.exists() is False

    for not_colaboradores_user in [publicador_user, revisor_user]:
        client.force_login(not_colaboradores_user)

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
            client=client,
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
        == f"Tema #{tema.id} foi deletado com sucesso."
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


@pytest.mark.django_db
def test_deve_editar_pergunta(client_with_login, user, mocker_request_get):
    pergunta = baker.make(
        "Pergunta",
        criado_por=user,
        tipo_resposta=inputs.TipoRespostaEnum.RLC.name,
        referencia_biblica=False,
        aprovado_status=False,
    )
    tema = baker.make("Tema", _fill_optional=True)

    resultado = graphql_query(
        query=eg.editar_pergunta_mutation,
        operation_name="editarPergunta",
        variables={
            "perguntaId": pergunta.id,
            "novoTemaId": tema.id,
            "novoEnunciado": "testenovoenunciando",
            "novoTipoResposta": inputs.TipoRespostaEnum.MES.name,
            "novoReferencia": "novaReferencia",
            "novoReferenciaBiblica": True,
            "novoAlternativas": [],
        },
        client=client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.enunciado == "testenovoenunciando"
    assert pergunta.tema == tema
    assert pergunta.tipo_resposta == inputs.TipoRespostaEnum.MES.name
    assert pergunta.referencia == "novaReferencia"
    assert pergunta.referencia_biblica is True
    assert mocker_request_get.called is True


@pytest.mark.django_db
def test_admin_deve_editar_pergunta(admin_client_with_login, user, mocker_request_get):
    pergunta = baker.make(
        "Pergunta",
        criado_por=user,
        tipo_resposta=inputs.TipoRespostaEnum.RLC.name,
        referencia_biblica=False,
        aprovado_status=False,
    )
    tema = baker.make("Tema", _fill_optional=True)

    resultado = graphql_query(
        query=eg.editar_pergunta_mutation,
        operation_name="editarPergunta",
        variables={
            "perguntaId": pergunta.id,
            "novoTemaId": tema.id,
            "novoEnunciado": "testenovoenunciando",
            "novoTipoResposta": inputs.TipoRespostaEnum.MES.name,
            "novoReferencia": "novaReferencia",
            "novoReferenciaBiblica": True,
            "novoAlternativas": [],
        },
        client=admin_client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.enunciado == "testenovoenunciando"
    assert pergunta.tema == tema
    assert pergunta.tipo_resposta == inputs.TipoRespostaEnum.MES.name
    assert pergunta.referencia == "novaReferencia"
    assert pergunta.referencia_biblica is True
    assert mocker_request_get.called is True


@pytest.mark.django_db
def test_nao_deve_editar_quando_user_nao_for_o_mesmo_que_criou_a_pergunta(
    client, user, mocker_request_get
):
    pergunta = baker.make(
        "Pergunta",
        criado_por=user,
        tipo_resposta=inputs.TipoRespostaEnum.RLC.name,
        referencia_biblica=False,
        aprovado_status=False,
        tema=baker.make("Tema"),
    )
    tema = baker.make("Tema", _fill_optional=True)

    other_user = baker.make("core.User", __fill_optional=True)
    client_with_user = client.force_login(other_user)

    resultado = graphql_query(
        query=eg.editar_pergunta_mutation,
        operation_name="editarPergunta",
        variables={
            "perguntaId": pergunta.id,
            "novoTemaId": tema.id,
            "novoEnunciado": "testenovoenunciando",
            "novoTipoResposta": inputs.TipoRespostaEnum.MES.name,
            "novoReferencia": "novaReferencia",
            "novoReferenciaBiblica": True,
            "novoAlternativas": [],
        },
        client=client_with_user,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.tema != tema
    assert pergunta.tipo_resposta == inputs.TipoRespostaEnum.RLC.name
    assert pergunta.referencia_biblica is False
    assert mocker_request_get.called is False


@pytest.mark.django_db
def test_nao_deve_editar_quando_nova_referencia_nao_for_valida(
    client_with_login, user, mocker_request_get_error
):
    pergunta = baker.make(
        "Pergunta",
        criado_por=user,
        tipo_resposta=inputs.TipoRespostaEnum.RLC.name,
        referencia_biblica=False,
        aprovado_status=False,
        tema=baker.make("Tema"),
    )
    tema = baker.make("Tema", _fill_optional=True)

    resultado = graphql_query(
        query=eg.editar_pergunta_mutation,
        operation_name="editarPergunta",
        variables={
            "perguntaId": pergunta.id,
            "novoTemaId": tema.id,
            "novoEnunciado": "testenovoenunciando",
            "novoTipoResposta": inputs.TipoRespostaEnum.MES.name,
            "novoReferencia": "novaReferencia",
            "novoReferenciaBiblica": True,
            "novoAlternativas": [],
        },
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.tema != tema
    assert pergunta.tipo_resposta == inputs.TipoRespostaEnum.RLC.name
    assert pergunta.referencia_biblica is False
    assert mocker_request_get_error.called is True


@pytest.mark.django_db
def test_nao_deve_editar_quando_pergunta_ja_tiver_sido_aprovada(
    client_with_login, user, mocker_request_get
):
    pergunta = baker.make(
        "Pergunta",
        criado_por=user,
        tipo_resposta=inputs.TipoRespostaEnum.RLC.name,
        referencia_biblica=False,
        aprovado_status=True,
        tema=baker.make("Tema"),
    )
    tema = baker.make("Tema", _fill_optional=True)

    resultado = graphql_query(
        query=eg.editar_pergunta_mutation,
        operation_name="editarPergunta",
        variables={
            "perguntaId": pergunta.id,
            "novoTemaId": tema.id,
            "novoEnunciado": "testenovoenunciando",
            "novoTipoResposta": inputs.TipoRespostaEnum.MES.name,
            "novoReferencia": "novaReferencia",
            "novoReferenciaBiblica": True,
            "novoAlternativas": [],
        },
        client=client_with_login,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.tema != tema
    assert pergunta.tipo_resposta == inputs.TipoRespostaEnum.RLC.name
    assert pergunta.referencia_biblica is False
    assert mocker_request_get.called is False


@pytest.mark.django_db
def test_deve_editar_perguntas_e_alternativas(
    client_with_login, user, mocker_request_get
):
    pergunta = baker.make(
        "Pergunta",
        criado_por=user,
        tipo_resposta=inputs.TipoRespostaEnum.RLC.name,
        referencia_biblica=False,
        aprovado_status=False,
    )
    alternativa1 = baker.make("Alternativa", pergunta=pergunta, __fill_optional=True)
    alternativa2 = baker.make("Alternativa", pergunta=pergunta, __fill_optional=True)

    resultado = graphql_query(
        query=eg.editar_pergunta_mutation,
        operation_name="editarPergunta",
        variables={
            "perguntaId": pergunta.id,
            "novoAlternativas": [
                {
                    "alternativaId": alternativa1.id,
                    "novoTexto": "London",
                    "novoCorreta": False,
                },
            ],
        },
        client=client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    alternativa1.refresh_from_db()
    alternativa2.refresh_from_db()
    assert pergunta.alternativas.count() == 2
    assert alternativa1.texto == "London"
    assert alternativa1.correta is False
    assert mocker_request_get.called is False


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_deve_aprovar_pergunta(client, revisor_user):
    pergunta = baker.make(
        "Pergunta", aprovado_por=None, aprovado_status=False, aprovado_em=None
    )

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.aprovar_pergunta_mutation,
        operation_name="aprovarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.aprovado_por == revisor_user
    assert pergunta.aprovado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.aprovado_status is True


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_deve_aprovar_pergunta_caso_usuario_seja_admin(client, admin_user):
    pergunta = baker.make(
        "Pergunta", aprovado_por=None, aprovado_status=False, aprovado_em=None
    )

    client.force_login(admin_user)

    resultado = graphql_query(
        query=eg.aprovar_pergunta_mutation,
        operation_name="aprovarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.aprovado_por == admin_user
    assert pergunta.aprovado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.aprovado_status is True


@pytest.mark.django_db
def test_nao_deve_aprovar_pergunta_caso_ja_tenha_sido_aprovada(client, revisor_user):
    pergunta = baker.make(
        "Pergunta", aprovado_por=None, aprovado_status=True, aprovado_em=None
    )

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.aprovar_pergunta_mutation,
        operation_name="aprovarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.aprovado_por is None
    assert pergunta.aprovado_em is None
    assert pergunta.aprovado_status is True


@pytest.mark.django_db
def test_nao_deve_aprovar_pergunta_caso_tenha_sido_criada_pelo_proprio_usuario(
    client, revisor_user
):
    pergunta = baker.make("Pergunta", aprovado_status=False, criado_por=revisor_user)

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.aprovar_pergunta_mutation,
        operation_name="aprovarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.aprovado_por is None
    assert pergunta.aprovado_em is None
    assert pergunta.aprovado_status is False


@pytest.mark.django_db
def test_nao_deve_aprovar_caso_usuario_nao_tenha_permissao(
    client, publicador_user, user
):
    unauthorized_users = [user, publicador_user]
    for current_user in unauthorized_users:
        pergunta = baker.make(
            "Pergunta", aprovado_por=None, aprovado_status=False, aprovado_em=None
        )

        client.force_login(current_user)

        resultado = graphql_query(
            query=eg.aprovar_pergunta_mutation,
            operation_name="aprovarPergunta",
            variables={"perguntaId": pergunta.id},
            client=client,
        )

        assert "errors" in json.loads(resultado.content)

        pergunta.refresh_from_db()
        assert pergunta.aprovado_por is None
        assert pergunta.aprovado_em is None
        assert pergunta.aprovado_status is False


@pytest.mark.django_db
def test_nao_deve_aprovar_caso_usuario_seja_anonimo(client):
    pergunta = baker.make(
        "Pergunta", aprovado_por=None, aprovado_status=False, aprovado_em=None
    )

    resultado = graphql_query(
        query=eg.aprovar_pergunta_mutation,
        operation_name="aprovarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.aprovado_por is None
    assert pergunta.aprovado_em is None
    assert pergunta.aprovado_status is False


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_admin_deve_aprovar_pergunta_recusada(client, admin_user):
    pergunta = baker.make(
        "Pergunta",
        aprovado_por=None,
        aprovado_status=False,
        aprovado_em=None,
        recusado_status=True,
    )

    client.force_login(admin_user)

    resultado = graphql_query(
        query=eg.aprovar_pergunta_mutation,
        operation_name="aprovarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.aprovado_por == admin_user
    assert pergunta.aprovado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.aprovado_status is True
    assert pergunta.recusado_status is False


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_nao_deve_aprovar_pergunta_recusada_caso_nao_seja_admin(client, revisor_user):
    pergunta = baker.make(
        "Pergunta",
        aprovado_por=None,
        aprovado_status=False,
        aprovado_em=None,
        recusado_status=True,
    )

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.aprovar_pergunta_mutation,
        operation_name="aprovarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.aprovado_por is None
    assert pergunta.aprovado_em is None
    assert pergunta.aprovado_status is False
    assert pergunta.recusado_status is True


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_deve_recusar_pergunta(client, revisor_user):
    pergunta = baker.make(
        "Pergunta", recusado_por=None, recusado_status=False, recusado_em=None
    )

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.recusar_pergunta_mutation,
        operation_name="recusarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.recusado_por == revisor_user
    assert pergunta.recusado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.recusado_status is True


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_deve_recusar_pergunta_caso_usuario_seja_admin(client, admin_user):
    pergunta = baker.make(
        "Pergunta", recusado_por=None, recusado_status=False, recusado_em=None
    )

    client.force_login(admin_user)

    resultado = graphql_query(
        query=eg.recusar_pergunta_mutation,
        operation_name="recusarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.recusado_por == admin_user
    assert pergunta.recusado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.recusado_status is True


@pytest.mark.django_db
def test_nao_deve_recusar_pergunta_caso_ja_tenha_sido_recusada(client, revisor_user):
    pergunta = baker.make(
        "Pergunta", recusado_por=None, recusado_status=True, recusado_em=None
    )

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.recusar_pergunta_mutation,
        operation_name="recusarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.recusado_por is None
    assert pergunta.recusado_em is None
    assert pergunta.recusado_status is True


@pytest.mark.django_db
def test_nao_deve_reprovar_pergunta_caso_tenha_sido_criada_pelo_proprio_usuario(
    client, revisor_user
):
    pergunta = baker.make("Pergunta", recusado_status=False, criado_por=revisor_user)

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.recusar_pergunta_mutation,
        operation_name="recusarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.recusado_por is None
    assert pergunta.recusado_em is None
    assert pergunta.recusado_status is False


@pytest.mark.django_db
def test_nao_deve_recusar_caso_usuario_nao_tenha_permissao(
    client, publicador_user, user
):
    unauthorized_users = [user, publicador_user]
    for current_user in unauthorized_users:
        pergunta = baker.make(
            "Pergunta", recusado_por=None, recusado_status=False, recusado_em=None
        )

        client.force_login(current_user)

        resultado = graphql_query(
            query=eg.recusar_pergunta_mutation,
            operation_name="recusarPergunta",
            variables={"perguntaId": pergunta.id},
            client=client,
        )

        assert "errors" in json.loads(resultado.content)

        pergunta.refresh_from_db()
        assert pergunta.recusado_por is None
        assert pergunta.recusado_em is None
        assert pergunta.recusado_status is False


@pytest.mark.django_db
def test_nao_deve_recusar_caso_usuario_seja_anonimo(client):
    pergunta = baker.make(
        "Pergunta", recusado_por=None, recusado_status=False, recusado_em=None
    )

    resultado = graphql_query(
        query=eg.recusar_pergunta_mutation,
        operation_name="recusarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.recusado_por is None
    assert pergunta.recusado_em is None
    assert pergunta.recusado_status is False


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_admin_deve_recusar_pergunta_aprovada_e_publicada(client, admin_user):
    pergunta = baker.make(
        "Pergunta",
        recusado_por=None,
        recusado_status=False,
        recusado_em=None,
        aprovado_status=True,
        publicado_status=True,
    )

    client.force_login(admin_user)

    resultado = graphql_query(
        query=eg.recusar_pergunta_mutation,
        operation_name="recusarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.recusado_por == admin_user
    assert pergunta.recusado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.recusado_status is True
    assert pergunta.aprovado_status is False
    assert pergunta.publicado_status is False


@pytest.mark.django_db
def test_nao_deve_recusar_pergunta_aprovada_caso_nao_seja_admin(client, revisor_user):
    pergunta = baker.make(
        "Pergunta",
        recusado_por=None,
        recusado_status=False,
        recusado_em=None,
        aprovado_status=True,
        publicado_status=True,
    )

    client.force_login(revisor_user)

    resultado = graphql_query(
        query=eg.recusar_pergunta_mutation,
        operation_name="recusarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.publicado_por is None
    assert pergunta.publicado_em is None
    assert pergunta.aprovado_status is True
    assert pergunta.publicado_status is True
    assert pergunta.recusado_status is False


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_deve_publicar_pergunta(client, publicador_user):
    pergunta = baker.make("Pergunta", recusado_status=False, aprovado_status=True)

    client.force_login(publicador_user)

    resultado = graphql_query(
        query=eg.publicar_pergunta_mutation,
        operation_name="publicarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.publicado_por == publicador_user
    assert pergunta.publicado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.publicado_status is True


@freeze_time("2012-01-14 12:00:01 +00:00")
@pytest.mark.django_db
def test_deve_publicar_pergunta_caso_usuario_seja_admin(client, admin_user):
    pergunta = baker.make("Pergunta", recusado_status=False, aprovado_status=True)

    client.force_login(admin_user)

    resultado = graphql_query(
        query=eg.publicar_pergunta_mutation,
        operation_name="publicarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.publicado_por == admin_user
    assert pergunta.publicado_em.isoformat() == "2012-01-14T12:00:01+00:00"
    assert pergunta.publicado_status is True


@pytest.mark.django_db
def test_nao_deve_publicar_pergunta_caso_ja_tenha_sido_recusada(
    client, publicador_user
):
    pergunta = baker.make("Pergunta", recusado_status=True, aprovado_status=False)

    client.force_login(publicador_user)

    resultado = graphql_query(
        query=eg.publicar_pergunta_mutation,
        operation_name="publicarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.publicado_por is None
    assert pergunta.publicado_em is None
    assert pergunta.publicado_status is False
    assert pergunta.recusado_status is True


@pytest.mark.django_db
def test_nao_deve_publicar_pergunta_caso_tenha_sido_criada_pelo_proprio_usuario(
    client, publicador_user
):
    pergunta = baker.make("Pergunta", criado_por=publicador_user, aprovado_status=True)

    client.force_login(publicador_user)

    resultado = graphql_query(
        query=eg.publicar_pergunta_mutation,
        operation_name="publicarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.publicado_por is None
    assert pergunta.publicado_em is None
    assert pergunta.publicado_status is False


@pytest.mark.django_db
def test_nao_deve_publicar_caso_usuario_nao_tenha_permissao(client, revisor_user, user):
    unauthorized_users = [user, revisor_user]
    for current_user in unauthorized_users:
        pergunta = baker.make("Pergunta", recusado_status=False, aprovado_status=True)

        client.force_login(current_user)

        resultado = graphql_query(
            query=eg.publicar_pergunta_mutation,
            operation_name="publicarPergunta",
            variables={"perguntaId": pergunta.id},
            client=client,
        )

        assert "errors" in json.loads(resultado.content)

        pergunta.refresh_from_db()
        assert pergunta.publicado_por is None
        assert pergunta.publicado_em is None
        assert pergunta.publicado_status is False


@pytest.mark.django_db
def test_nao_deve_publicar_caso_usuario_seja_anonimo(client):
    pergunta = baker.make("Pergunta", recusado_status=False, aprovado_status=True)

    resultado = graphql_query(
        query=eg.publicar_pergunta_mutation,
        operation_name="publicarPergunta",
        variables={"perguntaId": pergunta.id},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    pergunta.refresh_from_db()
    assert pergunta.publicado_por is None
    assert pergunta.publicado_em is None
    assert pergunta.publicado_status is False
