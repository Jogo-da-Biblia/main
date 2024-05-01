import pytest
import json
from app.core.models import User
from app.graphql.eg import novo_usuario_mutation


@pytest.mark.django_db
def test_deve_criar_novo_usuario(client_graphql):
    resultado = client_graphql(query=novo_usuario_mutation, operation_name="cadastrarUsuario", variables={"email":"teste1@email.com", "password": "senhateste123", "username": "ususaroteste1", "isStaff": False})

    assert 'errors' not in json.loads(resultado.content)
    assert User.objects.filter(email='teste1@email.com').exists()

    new_user = User.objects.get(username='ususaroteste1')
    assert new_user.username == 'ususaroteste1'
    assert new_user.check_password("senhateste123")
    assert new_user.is_staff is False



# @pytest.mark.django_db
# def test_deve_editar_novo_usuario(client, usuario_admin, criar_dados_de_teste):
#     new_user = User.objects.create(
#         email='edit@email.com', username='donoteditthis', is_staff=False)
#     user_id = new_user.id

#     assert new_user.username == 'donoteditthis'
#     assert new_user.email == 'edit@email.com'

#     resultado = client.execute(editar_usuario_mutation, variables={
#                                'userId': user_id}, context_value=UsuarioEmContexto(usuario=usuario_admin))

#     assert User.objects.filter(id=user_id).exists() == True

#     new_user.refresh_from_db()

#     assert resultado == {'data': OrderedDict([('editarUsuario', {'usuario': {
#                                              'id': f'{new_user.id}', 'username': 'newusername', 'email': 'newemai1l@.com'}})])}
#     assert new_user.username == 'newusername'
#     assert new_user.email == 'newemai1l@.com'
#     assert 'errors' not in resultado


# @pytest.mark.django_db
# def test_deve_enviar_email_com_nova_senha(client, usuario_admin):
#     new_user = User.objects.create(
#         email='user@email.com', username='donoteditthis', is_staff=False)
#     user_id = new_user.id

#     resultado = client.execute(reenviar_senha_mutation, variables={
#                                'userId': user_id}, context_value=UsuarioEmContexto(usuario=usuario_admin))

#     assert resultado == {'data': OrderedDict(
#         [('recuperarSenha', {'mensagem': 'Senha alterada e email enviado com sucesso'})])}
#     assert 'errors' not in resultado


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
