import json

import pytest
from app.core.models import User
from app.graphql import eg
from graphene_django.utils.testing import graphql_query


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
    assert new_user.is_staff is False
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
        client=client
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


# @pytest.mark.django_db
# def test_administrador_deve_receber_info_de_user_pelo_id(client, usuario_admin):
#     usuario_de_teste = User.objects.create(
#         username='user1', email='getuser@example.com', password='123456')

#     resultado = client.execute(query_usuario, variables={
#                                'userId': usuario_de_teste.id}, context_value=UsuarioEmContexto(usuario=usuario_admin))

#     assert resultado == {'data': {'user': {'id': str(usuario_de_teste.id), 'username': str(usuario_de_teste.username), 'email': str(
#         usuario_de_teste.email), 'pontuacao': 0, 'perguntasCriadas': [], 'perguntasRevisadas': [], 'perguntasPublicadas': []}}}
#     assert 'errors' not in resultado


# @pytest.mark.django_db
# def test_administrador_deve_receber_info_propria_se_user_for_vazio(client, usuario_admin):
#     resultado = client.execute(
#         usuario_vazio_query, context_value=UsuarioEmContexto(usuario=usuario_admin))

#     assert resultado == {'data': {'user': {'id': str(usuario_admin.id), 'username': str(usuario_admin.username), 'email': str(
#         usuario_admin.email), 'pontuacao': 0, 'perguntasCriadas': [], 'perguntasRevisadas': [], 'perguntasPublicadas': []}}}
#     assert 'errors' not in resultado


# @pytest.mark.django_db
# def test_admin_deve_listar_todos_usuarios(client, usuario_admin):
#     User.objects.create(
#         username='user5', email='oneuser@example.com', password='123456')
#     User.objects.create(
#         username='user6', email='twouser@example.com', password='123456')
#     User.objects.create(
#         username='user7', email='threeuser@example.com', password='123456')

#     resultado = client.execute(
#         query_usuarios, context_value=UsuarioEmContexto(usuario=usuario_admin))

#     assert resultado == {'data': {'users': [{'id': '4', 'username': 'admin', 'pontuacao': 0}, {'id': '5', 'username': 'user5', 'pontuacao': 0}, {
#         'id': '6', 'username': 'user6', 'pontuacao': 0}, {'id': '7', 'username': 'user7', 'pontuacao': 0}]}}
#     assert len(resultado['data']['users']) == len(User.objects.all())
#     assert 'errors' not in resultado
