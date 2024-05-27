import json

import pytest
from app.core.views import Role, Action
from app.core.models import User
from app.graphql import eg
from graphene_django.utils.testing import graphql_query
from model_bakery import baker


@pytest.mark.django_db
def test_deve_criar_novo_usuario(client_graphql_without_login):
    resultado = client_graphql_without_login(
        query=eg.novo_usuario_mutation,
        operation_name="cadastrarUsuario",
        variables={
            "email": "teste1@email.com",
            "password": "senhateste123",
            "username": "ususaroteste1",
            "name": "nome teste",
            "phone": "12345678",
            "isWhatsapp": True,
        },
    )

    assert "errors" not in json.loads(resultado.content)
    assert User.objects.filter(email="teste1@email.com").exists()

    new_user = User.objects.get(username="ususaroteste1")
    assert new_user.username == "ususaroteste1"
    assert new_user.name == "nome teste"
    assert new_user.phone == "12345678"
    assert new_user.is_whatsapp is True
    assert new_user.check_password("senhateste123")


@pytest.mark.django_db
def test_deve_editar_usuario(client, user):
    user.set_password("senhamudar")
    user.save()

    client.force_login(user)

    resultado = graphql_query(
        query=eg.editar_usuario_mutation,
        operation_name="editarUsuario",
        variables={
            "userId": user.id,
            "email": "novo@email.com",
            "password": "senhateste123",
            "username": "ususaroteste1",
            "name": "nome teste",
            "phone": "12345678",
            "isWhatsapp": True,
        },
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)
    user.refresh_from_db()

    assert user.username == "ususaroteste1"
    assert user.email == "novo@email.com"
    assert user.name == "nome teste"
    assert user.phone == "12345678"
    assert user.is_whatsapp is True
    assert user.check_password("senhateste123")


@pytest.mark.django_db
def test_usuario_admin_deve_editar_usuario(admin_client_with_login):
    new_user = User.objects.create(
        email="edit@email.com",
        username="donoteditthis",
        name="outro nome",
        phone="12345678",
        is_whatsapp=False,
    )
    new_user.set_password("senhamudar")
    new_user.save()
    user_id = new_user.id

    resultado = graphql_query(
        query=eg.editar_usuario_mutation,
        operation_name="editarUsuario",
        variables={
            "userId": user_id,
            "email": "novo@email.com",
            "password": "senhateste123",
            "username": "ususaroteste1",
            "name": "nome teste",
            "phone": "12345678",
            "isWhatsapp": True,
        },
        client=admin_client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)
    new_user.refresh_from_db()

    assert new_user.username == "ususaroteste1"
    assert new_user.email == "novo@email.com"
    assert new_user.name == "nome teste"
    assert new_user.phone == "12345678"
    assert new_user.is_whatsapp is True
    assert new_user.check_password("senhateste123")


@pytest.mark.django_db
def test_outro_usuario_nao_deve_editar_outro_usuario(client_graphql_with_login):
    new_user = User.objects.create(email="edit@email.com", username="donoteditthis")
    new_user.set_password("senhamudar")
    new_user.save()
    user_id = new_user.id

    resultado = client_graphql_with_login(
        query=eg.editar_usuario_mutation,
        operation_name="editarUsuario",
        variables={
            "userId": user_id,
            "newUsername": "NovoUsername",
            "newEmail": "novo@email.com",
            "newPassword": "newPassword",
        },
    )

    assert "errors" in json.loads(resultado.content)
    new_user.refresh_from_db()

    assert new_user.username == "donoteditthis"
    assert new_user.email == "edit@email.com"
    assert new_user.check_password("senhamudar")


@pytest.mark.django_db
def test_deve_enviar_email_com_nova_senha(client, mocker, user):
    mocked_email = mocker.patch("app.core.views.send_mail")

    user.set_password("senhamudar")
    user.save()
    user_id = user.id

    client.force_login(user)

    resultado = graphql_query(
        query=eg.recuperar_senha_mutation,
        operation_name="recuperarSenha",
        variables={"userId": user_id, "email": user.email},
        client=client,
    )

    assert "errors" not in json.loads(resultado.content)
    assert "Senha alterada e email enviado com sucesso" in str(resultado.content)
    user.refresh_from_db()

    assert user.check_password("senhamudar") is False
    assert mocked_email.called is True


@pytest.mark.django_db
def test_nao_deve_enviar_email_com_nova_senha_caso_email_enviado_seja_diferente_do_cadastrado(
    client, mocker, user
):
    mocked_email = mocker.patch("app.core.views.send_mail")

    user.set_password("senhamudar")
    user.save()
    user_id = user.id

    client.force_login(user)

    resultado = graphql_query(
        query=eg.recuperar_senha_mutation,
        operation_name="recuperarSenha",
        variables={"userId": user_id, "email": "otheremail@gmail.com"},
        client=client,
    )

    assert "errors" in json.loads(resultado.content)
    assert "O email informado nao corresponde ao email cadastrado" in str(
        resultado.content
    )
    user.refresh_from_db()
    assert user.check_password("senhamudar") is True
    assert mocked_email.called is False


@pytest.mark.django_db
def test_deve_enviar_email_com_nova_senha_caso_usuario_seja_admin(
    mocker, admin_client_with_login, user
):
    mocked_email = mocker.patch("app.core.views.send_mail")

    user.set_password("senhamudar")
    user.save()
    user_id = user.id

    resultado = graphql_query(
        query=eg.recuperar_senha_mutation,
        operation_name="recuperarSenha",
        variables={"userId": user_id, "email": user.email},
        client=admin_client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)
    assert "Senha alterada e email enviado com sucesso" in str(resultado.content)
    user.refresh_from_db()

    assert user.check_password("senhamudar") is False
    assert mocked_email.called is True


@pytest.mark.parametrize(
    (
        "enum_selected",
        "admin_expected",
        "revisor_expected",
        "publicador_expected",
    ),
    [
        (Role.REVISOR.name, False, True, False),
        (Role.PUBLICADOR.name, False, False, True),
        (Role.ADMIN.name, True, False, False),
    ],
)
@pytest.mark.django_db
def test_usuario_admin_deve_adicionar_usuario_aos_grupos_solicitados(
    admin_client_with_login,
    enum_selected,
    admin_expected,
    revisor_expected,
    publicador_expected,
):
    new_user = baker.make("core.User", _fill_optional=True)
    user_id = new_user.id

    assert new_user.is_admin is False
    assert new_user.is_revisor is False
    assert new_user.is_publicador is False

    resultado = graphql_query(
        query=eg.alterar_permissoes_mutation,
        operation_name="alterarPermissoes",
        variables={
            "userId": user_id,
            "role": enum_selected,
            "action": Action.ADD.name,
        },
        client=admin_client_with_login,
    )

    assert "errors" not in json.loads(resultado.content)

    assert new_user.is_admin is admin_expected
    assert new_user.is_revisor is revisor_expected
    assert new_user.is_publicador is publicador_expected


# TODO
# Test logged dont do this
# Test anonymous dont do this
@pytest.mark.parametrize(
    "enum_selected",
    [
        Role.REVISOR.name,
        Role.PUBLICADOR.name,
        Role.ADMIN.name,
    ],
)
@pytest.mark.django_db
def test_usuario_anonimos_nao_deve_adicionar_usuario_aos_grupos_solicitados(
    client, enum_selected
):
    new_user = baker.make("core.User", _fill_optional=True)
    user_id = new_user.id

    assert new_user.is_admin is False
    assert new_user.is_revisor is False
    assert new_user.is_publicador is False

    resultado = graphql_query(
        query=eg.alterar_permissoes_mutation,
        operation_name="alterarPermissoes",
        variables={
            "userId": user_id,
            "role": enum_selected,
            "action": Action.ADD.name,
        },
        client=client,
    )

    assert "errors" in json.loads(resultado.content)

    assert new_user.is_admin is False
    assert new_user.is_revisor is False
    assert new_user.is_publicador is False


@pytest.mark.parametrize(
    "enum_selected",
    [
        Role.REVISOR.name,
        Role.PUBLICADOR.name,
        Role.ADMIN.name,
    ],
)
@pytest.mark.django_db
def test_usuario_não_admin_nao_deve_adicionar_usuario_aos_grupos_solicitados(
    client_graphql_with_login, enum_selected
):
    new_user = baker.make("core.User", _fill_optional=True)
    user_id = new_user.id

    assert new_user.is_admin is False
    assert new_user.is_revisor is False
    assert new_user.is_publicador is False

    resultado = client_graphql_with_login(
        query=eg.alterar_permissoes_mutation,
        operation_name="alterarPermissoes",
        variables={
            "userId": user_id,
            "role": enum_selected,
            "action": Action.ADD.name,
        },
    )

    assert "errors" in json.loads(resultado.content)

    assert new_user.is_admin is False
    assert new_user.is_revisor is False
    assert new_user.is_publicador is False

# TODO add remove test
# @pytest.mark.parametrize(
#     (
#         "enum_selected",
#         "admin_expected",
#         "revisor_expected",
#         "publicador_expected",
#     ),
#     [
#         (Role.REVISOR.name, False, True, False),
#         (Role.PUBLICADOR.name, False, False, True),
#         (Role.ADMIN.name, True, False, False),
#     ],
# )
# @pytest.mark.django_db
# def test_usuario_admin_deve_adicionar_usuario_aos_grupos_solicitados(
#     admin_client_with_login,
#     enum_selected,
#     admin_expected,
#     revisor_expected,
#     publicador_expected,
# ):
#     new_user = baker.make("core.User", _fill_optional=True)
#     user_id = new_user.id

#     assert new_user.is_admin is False
#     assert new_user.is_revisor is False
#     assert new_user.is_publicador is False

#     resultado = graphql_query(
#         query=eg.alterar_permissoes_mutation,
#         operation_name="alterarPermissoes",
#         variables={
#             "userId": user_id,
#             "role": enum_selected,
#             "action": Action.ADD.name,
#         },
#         client=admin_client_with_login,
#     )

#     assert "errors" not in json.loads(resultado.content)

#     assert new_user.is_admin is admin_expected
#     assert new_user.is_revisor is revisor_expected
#     assert new_user.is_publicador is publicador_expected


# # TODO
# # Test logged dont do this
# # Test anonymous dont do this
# @pytest.mark.parametrize(
#     "enum_selected",
#     [
#         Role.REVISOR.name,
#         Role.PUBLICADOR.name,
#         Role.ADMIN.name,
#     ],
# )
# @pytest.mark.django_db
# def test_usuario_anonimos_nao_deve_adicionar_usuario_aos_grupos_solicitados(
#     client, enum_selected
# ):
#     new_user = baker.make("core.User", _fill_optional=True)
#     user_id = new_user.id

#     assert new_user.is_admin is False
#     assert new_user.is_revisor is False
#     assert new_user.is_publicador is False

#     resultado = graphql_query(
#         query=eg.alterar_permissoes_mutation,
#         operation_name="alterarPermissoes",
#         variables={
#             "userId": user_id,
#             "role": enum_selected,
#             "action": Action.ADD.name,
#         },
#         client=client,
#     )

#     assert "errors" in json.loads(resultado.content)

#     assert new_user.is_admin is False
#     assert new_user.is_revisor is False
#     assert new_user.is_publicador is False


# @pytest.mark.parametrize(
#     "enum_selected",
#     [
#         Role.REVISOR.name,
#         Role.PUBLICADOR.name,
#         Role.ADMIN.name,
#     ],
# )
# @pytest.mark.django_db
# def test_usuario_não_admin_nao_deve_adicionar_usuario_aos_grupos_solicitados(
#     client_graphql_with_login, enum_selected
# ):
#     new_user = baker.make("core.User", _fill_optional=True)
#     user_id = new_user.id

#     assert new_user.is_admin is False
#     assert new_user.is_revisor is False
#     assert new_user.is_publicador is False

#     resultado = client_graphql_with_login(
#         query=eg.alterar_permissoes_mutation,
#         operation_name="alterarPermissoes",
#         variables={
#             "userId": user_id,
#             "role": enum_selected,
#             "action": Action.ADD.name,
#         },
#     )

#     assert "errors" in json.loads(resultado.content)

#     assert new_user.is_admin is False
#     assert new_user.is_revisor is False
#     assert new_user.is_publicador is False
