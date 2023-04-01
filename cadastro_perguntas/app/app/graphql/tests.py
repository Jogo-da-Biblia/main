import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

import pytest
from collections import OrderedDict
from graphene.test import Client as GrapheneClient
from app.core.models import User
from app.biblia.models import Livro, Versiculo, Testamento, Versao
from app.perguntas.models import Pergunta, Tema, Referencia
from django.core.exceptions import ObjectDoesNotExist
from .schema import schema
from .test_queries import querie_usuario, querie_usuarios, pergunta_aleatoria_querie, todas_perguntas_querie, usuario_vazio_querie, texto_biblico_querie, novo_usuario_mutation, editar_usuario_mutation, adicionar_nova_pergunta_mutation, editar_pergunta_mutation, reenviar_senha_mutation

# Usuario enviado no context graphql
class UsuarioEmContexto:
    def __init__(self, usuario):
        self.user = usuario


@pytest.fixture
def usuario_admin():
    try:
        usuario = User.objects.get(username='admin')
    except ObjectDoesNotExist:
        usuario = User.objects.create_superuser(username='admin', password='admin', email='admin@admin.com')
    return usuario

@pytest.fixture
def client():
    graphene_client = GrapheneClient(schema)
    return graphene_client

@pytest.fixture
def perguntas_count():
    return Pergunta.objects.count()

@pytest.fixture
def todas_perguntas():
    return Pergunta.objects.all()

@pytest.fixture
def delete_todos_items():
    Pergunta.objects.all().delete()
    Tema.objects.all().delete()
    Testamento.objects.all().delete()
    Versiculo.objects.all().delete()
    Versao.objects.all().delete()
    Livro.objects.all().delete()
    Referencia.objects.all().delete()

@pytest.fixture
def criar_dados_de_teste(usuario_admin, delete_todos_items):
    Tema.objects.create(nome='tema1', cor='rosa')
    Tema.objects.create(nome='tema2', cor='dois')
    

    test_livro = Livro(
        testamento=Testamento.objects.create(nome='testamento1'),
        posicao=1,
        nome='livro1',
        sigla='te1'
    )
    test_livro.save()

    test_versiculo = Versiculo.objects.create(
        versao=Versao.objects.create(nome='versaonome1', sigla='VER1'),
        livro=test_livro,
        capitulo=1,
        versiculo=21,
        texto='Versiculo texto'
    )
    test_versiculo.save()

    Referencia.objects.create(
        livro = test_livro,
        versiculo = test_versiculo
    )

    new_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema1'),
        enunciado = 'enunciado1adadasdasda',
        tipo_resposta = 'MES',
        criado_por = usuario_admin
    )

    another_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema2'),
        enunciado = 'enunciado2a',
        tipo_resposta = 'MES',
        criado_por = usuario_admin
    )
    
    new_pergunta.save()
    another_pergunta.save()
    return new_pergunta


@pytest.mark.django_db
def test_administrador_deve_receber_info_de_user_pelo_id(client, usuario_admin):
    test_user = User.objects.create(username='Get user', email='getuser@example.com', password='123456')

    query = querie_usuario.replace('user_id', str(test_user.id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'user': {'usuario': {'id': str(test_user.id), 'username': str(test_user.username), 'email': str(test_user.email)}, 'perguntas': []}}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_administrador_deve_receber_info_propria_se_user_for_vazio(client, usuario_admin):
    query = usuario_vazio_querie.replace('user_id', str(usuario_admin.id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'user': {'usuario': {'id': str(usuario_admin.id), 'username': str(usuario_admin.username), 'email': str(usuario_admin.email)}, 'perguntas': []}}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_admin_deve_listar_todos_usuarios(client, usuario_admin):
    User.objects.create(username='one user', email='oneuser@example.com', password='123456')
    User.objects.create(username='two user', email='twouser@example.com', password='123456')
    User.objects.create(username='three user', email='threeuser@example.com', password='123456')

    query = querie_usuarios

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert resultado == {'data': {'users': {'usuario': [{'id': '4', 'username': 'admin', 'pontuacao': 0}, {'id': '5', 'username': 'one user', 'pontuacao': 0}, {'id': '6', 'username': 'two user', 'pontuacao': 0}, {'id': '7', 'username': 'three user', 'pontuacao': 0}]}}}
    assert len(resultado['data']['users']['usuario']) == len(User.objects.all())
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_retornar_pergunta_aleatoria(client, criar_dados_de_teste, usuario_admin):
    query = pergunta_aleatoria_querie

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'pergunta': [{'id': '1', 'enunciado': 'enunciado1adadasdasda'}]}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_retornar_todas_as_perguntas(client, criar_dados_de_teste, usuario_admin, todas_perguntas):
    query = todas_perguntas_querie

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    
    assert resultado == {'data': {'perguntas': [{'id': f'{todas_perguntas[0].id}', 'enunciado': 'enunciado1adadasdasda'}, {'id': f'{todas_perguntas[1].id}', 'enunciado': 'enunciado2a'}]}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_buscar_texto_biblico(client, usuario_admin, criar_dados_de_teste):
    query = texto_biblico_querie

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'textoBiblico': {'textos': [{'livro': 'livro1', 'livroAbreviado': 'te1', 'versao': 'versaonome1', 'versaoAbreviada': 'VER1', 'capitulo': 1, 'versiculo': 21, 'texto': 'Versiculo texto'}]}}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_criar_novo_usuario(client, usuario_admin):
    query = novo_usuario_mutation

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert User.objects.filter(email='teste1@email.com').exists() == True
    
    new_user = User.objects.get(username='ususaroteste1')

    assert resultado == {'data': OrderedDict([('cadastrarUsuario', {'usuario': {'id': str(new_user.id), 'email': str(new_user.email)}})])}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_editar_novo_usuario(client, usuario_admin, criar_dados_de_teste):
    new_user = User.objects.create(email='edit@email.com', username='donoteditthis', is_staff=False)
    user_id = new_user.id

    assert new_user.username == 'donoteditthis'
    assert new_user.email == 'edit@email.com'

    query = editar_usuario_mutation.replace('user_id', str(user_id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    
    assert User.objects.filter(id=user_id).exists() == True

    new_user.refresh_from_db()
    
    assert resultado == {'data': OrderedDict([('editarUsuario', {'usuario': {'id': f'{new_user.id}', 'username': 'newusername', 'email': 'newemai1l@.com'}})])}
    assert new_user.username == 'newusername'
    assert new_user.email == 'newemai1l@.com'
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_enviar_email_com_nova_senha(client, usuario_admin):
    new_user = User.objects.create(email='user@email.com', username='donoteditthis', is_staff=False)
    user_id = new_user.id

    query = reenviar_senha_mutation.replace('user_id', str(user_id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    
    assert resultado == {'data': OrderedDict([('recuperarSenha', {'mensagem': 'Senha alterada e email enviado com sucesso'})])}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_adicionar_nova_pergunta(client, usuario_admin, criar_dados_de_teste):
    tema_id = Tema.objects.get(nome='tema1').id
    referencia_id = Referencia.objects.all()[0].id
    
    query = adicionar_nova_pergunta_mutation.replace('tema_id', str(tema_id)).replace('referencia_id', str(referencia_id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    newest_pergunta = Pergunta.objects.last()
    assert resultado == {'data': OrderedDict([('cadastrarPergunta', {'pergunta': {'id': f'{newest_pergunta.id}', 'tema': {'nome': 'tema1'}, 'enunciado': 'Enunciaod da pergunta', 'tipoResposta': 'MES', 'status': False, 'revisadoPor': None}})])}
    assert len(Pergunta.objects.all()) == 3
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_editar_nova_pergunta(client, usuario_admin, criar_dados_de_teste):
    new_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema1'),
        enunciado = 'enunciado1adadasdasda',
        tipo_resposta = 'MES',
        criado_por = usuario_admin,
        status=False
    )
    pergunta_id = new_pergunta.id

    assert new_pergunta.enunciado == 'enunciado1adadasdasda'
    assert new_pergunta.status == False

    tema_id = Tema.objects.get(nome='tema1').id
    referencia_id = Referencia.objects.all()[0].id

    query = editar_pergunta_mutation.replace('tema_id', str(tema_id)).replace('referencia_id', str(referencia_id)).replace('pergunta_id', str(pergunta_id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    new_pergunta.refresh_from_db()

    assert resultado == {'data': OrderedDict([('editarPergunta', {'pergunta': {'id': f'{new_pergunta.id}', 'enunciado': 'Novo enunciado', 'revisadoPor': None, 'status': True}})])}
    assert new_pergunta.enunciado == 'Novo enunciado'
    assert new_pergunta.status == True
    assert 'errors' not in resultado