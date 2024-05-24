import json

import pytest
from app.core.models import User
from app.graphql import eg
from graphene_django.utils.testing import graphql_query
from django.contrib.auth.models import Group
from model_bakery import baker


@pytest.mark.django_db
def test_deve_listar_usuarios(admin_client_with_login, admin_user):
    user1 = baker.make("core.User", _fill_optional=True)
    user2 = baker.make("core.User", _fill_optional=True)
    user3 = baker.make("core.User", _fill_optional=True)

    resultado = graphql_query(query=eg.query_usuarios, client=admin_client_with_login)

    assert "errors" not in json.loads(resultado.content)

    assert {
        "id": str(user3.id),
        "username": str(user3.username),
        "email": str(user3.email),
    } in json.loads(resultado.content)["data"]["users"]
    
    assert {
        "id": str(admin_user.id),
        "username": str(admin_user.username),
        "email": str(admin_user.email),
    } in json.loads(resultado.content)["data"]["users"]
    
    assert {
        "id": str(user1.id),
        "username": str(user1.username),
        "email": str(user1.email),
    } in json.loads(resultado.content)["data"]["users"]

    assert {
        "id": str(user2.id),
        "username": str(user2.username),
        "email": str(user2.email),
    } in json.loads(resultado.content)["data"]["users"]


@pytest.mark.django_db
def test_nao_deve_listar_usuarios_quando_usuario_nao_estiver_logado(
    client_graphql_without_login,
):
    user1 = baker.make("core.User", _fill_optional=True)
    user2 = baker.make("core.User", _fill_optional=True)
    user3 = baker.make("core.User", _fill_optional=True)

    resultado = client_graphql_without_login(query=eg.query_usuarios)

    assert "errors" in json.loads(resultado.content)
    assert "permission" in str(json.loads(resultado.content))


@pytest.mark.django_db
def test_nao_deve_listar_usuarios_quando_usuario_nao_for_admin(
    client_graphql_with_login,
):
    user1 = baker.make("core.User", _fill_optional=True)
    user2 = baker.make("core.User", _fill_optional=True)
    user3 = baker.make("core.User", _fill_optional=True)

    resultado = client_graphql_with_login(query=eg.query_usuarios)

    assert "errors" in json.loads(resultado.content)


@pytest.mark.django_db
def test_deve_listar_informacoes_do_usuario_quando_usuario_for_ele_mesmo(
    client_graphql_with_login, user
):
    resultado = client_graphql_with_login(
        query=eg.query_usuario, variables={"userId": user.id}
    )

    assert "errors" not in json.loads(resultado.content)

    assert json.loads(resultado.content) == {
        "data": {
            "user": {
                "id": str(user.id),
                "username": str(user.username),
                "email": str(user.email),
                "isActive": user.is_active,
                "perguntasEnviadas": [],
                "perguntasRevisadas": [],
                "perguntasRecusadas": [],
                "perguntasPublicadas": [],
                "pontuacao": 0,
                "isAdmin": False,
                "isRevisor": False,
                "isPublicador": False,
            }
        }
    }


@pytest.mark.django_db
def test_deve_listar_informacoes_do_usuario_quando_usuario_for_admin(
    admin_client_with_login, user
):
    resultado = graphql_query(
        query=eg.query_usuario,
        variables={"userId": user.id},
        client=admin_client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    assert json.loads(resultado.content) == {
        "data": {
            "user": {
                "id": str(user.id),
                "username": str(user.username),
                "email": str(user.email),
                "isActive": user.is_active,
                "perguntasEnviadas": [],
                "perguntasRevisadas": [],
                "perguntasRecusadas": [],
                "perguntasPublicadas": [],
                "pontuacao": 0,
                "isAdmin": False,
                "isRevisor": False,
                "isPublicador": False,
            }
        }
    }


@pytest.mark.django_db
def test_deve_listar_informacoes_do_usuario_logado_quando_nao_enviar_nenhum_id(
    client_graphql_with_login, user
):
    resultado = client_graphql_with_login(
        query=eg.query_usuario,
        variables={"userId": user.id},
    )

    assert "errors" not in json.loads(resultado.content)

    assert User.objects.count() == 1
    assert json.loads(resultado.content) == {
        "data": {
            "user": {
                "id": str(user.id),
                "username": str(user.username),
                "email": str(user.email),
                "isActive": user.is_active,
                "perguntasEnviadas": [],
                "perguntasRevisadas": [],
                "perguntasRecusadas": [],
                "perguntasPublicadas": [],
                "pontuacao": 0,
                "isAdmin": False,
                "isRevisor": False,
                "isPublicador": False,
            }
        }
    }


@pytest.mark.django_db
def test_nao_deve_listar_informacoes_do_usuario_quando_nao_estiver_logado(
    client_graphql_without_login, user
):
    resultado = client_graphql_without_login(
        query=eg.query_usuario,
        variables={"userId": user.id},
    )

    assert "errors" in json.loads(resultado.content)
    assert "permission" in str(json.loads(resultado.content))


@pytest.mark.django_db
def test_nao_deve_listar_informacoes_do_usuario_quando_usuario_nao_for_ele_mesmo(
    client_graphql_with_login,
):
    other_user = baker.make("core.User", _fill_optional=True)

    resultado = client_graphql_with_login(
        query=eg.query_usuario, variables={"userId": other_user.id}
    )

    assert "errors" in json.loads(resultado.content)
    assert "Somente o proprio usuario e administradores" in str(
        json.loads(resultado.content)
    )


@pytest.mark.django_db
def criar_perguntas_para_teste(enviadas, revisadas, publicadas, recusadas, user):
    # Perguntas enviadas
    if enviadas != 0:
        baker.make("Pergunta", criado_por=user, _quantity=enviadas)

    # Perguntas recusadas
    if recusadas != 0:
        baker.make(
            "Pergunta",
            criado_por=user,
            recusado_por=user,
            recusado_status=True,
            _quantity=recusadas,
        )

    # Perguntas revisadas
    if revisadas != 0:
        baker.make(
            "Pergunta",
            criado_por=user,
            revisado_por=user,
            revisado_status=True,
            _quantity=revisadas,
        )

    # Perguntas Publicadas
    if publicadas != 0:
        baker.make(
            "Pergunta",
            criado_por=user,
            revisado_status=True,
            publicado_por=user,
            _quantity=publicadas,
        )

    return None


@pytest.mark.parametrize(
    (
        "perguntas_enviadas",
        "perguntas_revisadas",
        "perguntas_publicadas",
        "perguntas_recusadas",
        "pontuacao_esperada",
    ),
    [
        (1, 1, 1, 1, 7),
        (4, 3, 2, 1, 17),
        (10, 0, 5, 2, 27),
        (3, 7, 0, 5, 22),
        (6, 2, 3, 0, 19),
        (2, 3, 4, 5, 25),
    ],
)
@pytest.mark.django_db
def test_deve_listar_pontuacao_do_usuario_corretamente(
    client_graphql_with_login,
    user,
    perguntas_enviadas,
    perguntas_revisadas,
    perguntas_publicadas,
    perguntas_recusadas,
    pontuacao_esperada,
):
    criar_perguntas_para_teste(
        enviadas=perguntas_enviadas,
        revisadas=perguntas_revisadas,
        publicadas=perguntas_publicadas,
        recusadas=perguntas_recusadas,
        user=user,
    )

    resultado = client_graphql_with_login(
        query=eg.query_usuario, variables={"userId": user.id}
    )

    assert "errors" not in json.loads(resultado.content)
    assert (
        json.loads(resultado.content)["data"]["user"]["pontuacao"] == pontuacao_esperada
    )


@pytest.mark.django_db
def test_deve_listar_pontuacao_do_usuario_corretamente_e_ignorar_perguntas_com_status_recusado(
    client_graphql_with_login,
    user,
):
    # Pergunta eviada
    baker.make("Pergunta", criado_por=user)

    # Pergunta com status revisada porém recusada
    baker.make(
        "Pergunta",
        criado_por=user,
        revisado_por=user,
        revisado_status=True,
        recusado_por=user,
        recusado_status=True,
    )

    # Pergunta publicada porém recusada
    baker.make(
        "Pergunta",
        criado_por=user,
        revisado_status=True,
        publicado_por=user,
        recusado_por=user,
        recusado_status=True,
    )

    resultado = client_graphql_with_login(
        query=eg.query_usuario, variables={"userId": user.id}
    )

    assert "errors" not in json.loads(resultado.content)
    assert json.loads(resultado.content)["data"]["user"]["pontuacao"] == 3


@pytest.mark.django_db
def test_deve_listar_pontuacao_do_usuario_corretamente_e_ignorar_perguntas_publicada_sem_estarem_revisadas(
    client_graphql_with_login,
    user,
):
    # Pergunta eviada
    baker.make("Pergunta", criado_por=user)

    # Pergunta com status revisada porém recusada
    baker.make(
        "Pergunta",
        criado_por=user,
        revisado_por=user,
        revisado_status=True,
    )

    # Pergunta publicada porém sem o status revisada
    baker.make(
        "Pergunta",
        criado_por=user,
        revisado_status=False,
        publicado_por=user,
    )

    resultado = client_graphql_with_login(
        query=eg.query_usuario, variables={"userId": user.id}
    )

    assert "errors" not in json.loads(resultado.content)
    assert json.loads(resultado.content)["data"]["user"]["pontuacao"] == 4


@pytest.mark.parametrize(
    (
        "admin_expected",
        "revisor_expected",
        "publicador_expected",
    ),
    [
        (True, True, True),
        (False, True, False),
        (False, False, False),
        (False, False, True),
    ],
)
@pytest.mark.django_db
def test_deve_mostrar_permissoes_do_usuario(
    client_graphql_with_login,
    user, admin_expected, revisor_expected, publicador_expected
):
    admin_group, _ = Group.objects.get_or_create(name="administradores")
    revisor_group, _ = Group.objects.get_or_create(name="revisores")
    publicador_group, _ = Group.objects.get_or_create(name="publicadores")

    if admin_expected is True:
        user.groups.add(admin_group)
    if revisor_expected is True:
        user.groups.add(revisor_group)
    if publicador_expected is True:
        user.groups.add(publicador_group)

    
    resultado = client_graphql_with_login(
        query=eg.query_usuario, variables={"userId": user.id}
    )

    assert "errors" not in json.loads(resultado.content)
    assert (
        json.loads(resultado.content)["data"]["user"]["isAdmin"] is admin_expected
    )
    assert (
        json.loads(resultado.content)["data"]["user"]["isRevisor"] is revisor_expected
    )
    assert (
        json.loads(resultado.content)["data"]["user"]["isPublicador"] is publicador_expected
    )