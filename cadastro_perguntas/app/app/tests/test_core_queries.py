import json

import pytest
from app.core.models import User
from app.graphql import eg
from graphene_django.utils.testing import graphql_query
from model_bakery import baker


# TODO add tests
# user should return logged user data if user is logged and dont pass any id

# user should dont return user if user is not logged in
# user should dont return user data if user is different
# user should return user pontuation


@pytest.mark.django_db
def test_deve_listar_usuarios(admin_client_with_login, admin_user):
    user1 = baker.make("core.User", _fill_optional=True)
    user2 = baker.make("core.User", _fill_optional=True)
    user3 = baker.make("core.User", _fill_optional=True)

    resultado = graphql_query(query=eg.query_usuarios, client=admin_client_with_login)

    assert "errors" not in json.loads(resultado.content)

    assert json.loads(resultado.content) == {
        "data": {
            "users": [
                {
                    "id": str(user3.id),
                    "username": str(user3.username),
                    "email": str(user3.email),
                },
                {
                    "id": str(admin_user.id),
                    "username": str(admin_user.username),
                    "email": str(admin_user.email),
                },
                {
                    "id": str(user1.id),
                    "username": str(user1.username),
                    "email": str(user1.email),
                },
                {
                    "id": str(user2.id),
                    "username": str(user2.username),
                    "email": str(user2.email),
                },
            ]
        }
    }


@pytest.mark.django_db
def test_nao_deve_listar_usuarios_quando_usuario_nao_estiver_logado(
    client_graphql_without_login,
):
    user1 = baker.make("core.User", _fill_optional=True)
    user2 = baker.make("core.User", _fill_optional=True)
    user3 = baker.make("core.User", _fill_optional=True)

    resultado = client_graphql_without_login(query=eg.query_usuarios)

    assert "errors" in json.loads(resultado.content)


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
    client_graphql_with_login,
):
    current_user = User.objects.first()

    resultado = client_graphql_with_login(
        query=eg.query_usuario, variables={"userId": current_user.id}
    )

    assert "errors" not in json.loads(resultado.content)

    assert json.loads(resultado.content) == {
        "data": {
            "user": {
                "id": str(current_user.id),
                "username": str(current_user.username),
                "email": str(current_user.email),
                "isSuperuser": current_user.is_superuser,
                "isActive": current_user.is_active,
                "perguntasCriadas": [],
                "perguntasRevisadas": [],
                "perguntasPublicadas": [],
                "pontuacao": 0,
            }
        }
    }


@pytest.mark.django_db
def test_deve_listar_informacoes_do_usuario_quando_usuario_for_admin(
    admin_client_with_login, user
):
    resultado = graphql_query(
        query=eg.query_usuario, variables={"userId": user.id}, client=admin_client_with_login
    )

    assert "errors" not in json.loads(resultado.content)

    assert json.loads(resultado.content) == {
        "data": {
            "user": {
                "id": str(user.id),
                "username": str(user.username),
                "email": str(user.email),
                "isSuperuser": user.is_superuser,
                "isActive": user.is_active,
                "perguntasCriadas": [],
                "perguntasRevisadas": [],
                "perguntasPublicadas": [],
                "pontuacao": 0,
            }
        }
    }
