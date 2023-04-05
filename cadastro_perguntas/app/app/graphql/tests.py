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
from app.comentarios.models import Comentario
from django.core.exceptions import ObjectDoesNotExist
from .schema import schema
from .test_queries import querie_usuario, querie_usuarios, pergunta_aleatoria_querie, todas_perguntas_querie, usuario_vazio_querie, texto_biblico_querie, novo_usuario_mutation, editar_usuario_mutation, adicionar_nova_pergunta_mutation, editar_pergunta_mutation, reenviar_senha_mutation, todos_comentarios_querie, adicionar_comentario_mutation

# Prevents pytest from collecting the following classes as tests
Testamento.__test__ = False

# Usuario enviado no context graphql
class UsuarioEmContexto:
    def __init__(self, usuario):
        self.user = usuario


@pytest.fixture
def usuario_admin(db):
    try:
        usuario = User.objects.get(username='admin')
    except ObjectDoesNotExist:
        usuario = User.objects.create_superuser(username='admin', password='admin', email='admin@admin.com')
    return usuario

@pytest.fixture
def client(db):
    graphene_client = GrapheneClient(schema)
    return graphene_client

@pytest.fixture
def perguntas_count(db):
    return Pergunta.objects.count()

@pytest.fixture
def todas_perguntas(db):
    return Pergunta.objects.all()

@pytest.fixture
def todos_comentarios(db):
    return Comentario.objects.all()

@pytest.fixture
def delete_todos_items(db):
    Pergunta.objects.all().delete()
    Tema.objects.all().delete()
    Testamento.objects.all().delete()
    Versiculo.objects.all().delete()
    Versao.objects.all().delete()
    Livro.objects.all().delete()
    Referencia.objects.all().delete()
    Comentario.objects.all().delete()

@pytest.fixture
def criar_dados_de_teste(usuario_admin, delete_todos_items, db):
    Tema.objects.create(nome='tema1', cor='rosa')
    Tema.objects.create(nome='tema2', cor='dois')
    

    test_livro = Livro(
        testamento=Testamento.objects.create(nome='testamento1'),
        posicao=1,
        nome='livro1',
        sigla='te1'
    )
    test_livro.save()

    Livro.objects.create(
        testamento=Testamento.objects.create(nome='testamento2'),
        posicao=2,
        nome='livro2',
        sigla='te2'
    )

    test_versiculo = Versiculo.objects.create(
        versao=Versao.objects.create(nome='versaonome1', sigla='VER1'),
        livro=test_livro,
        capitulo=1,
        versiculo=21,
        texto='Versiculo texto'
    )
    test_versiculo.save()
    # Create 3 more versiculos
    for i in range(1,4):
        Versiculo.objects.create(
            versao=Versao.objects.get(nome='versaonome1', sigla='VER1'),
            livro=test_livro,
            capitulo=1,
            versiculo=21+i,
            texto='Versiculo texto'
        )
        Versiculo.objects.create(
            versao=Versao.objects.get(nome='versaonome1', sigla='VER1'),
            livro=Livro.objects.get(nome='livro2'),
            capitulo=1,
            versiculo=i,
            texto='Versiculo texto'
        )
    Versiculo.objects.create(
        versao=Versao.objects.get(nome='versaonome1', sigla='VER1'),
        livro=test_livro,
        capitulo=2,
        versiculo=4,
        texto='Versiculo texto'
        )

    Referencia.objects.create(
        livro = test_livro,
        versiculo = test_versiculo
    )

    nova_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema1'),
        enunciado = 'enunciado1adadasdasda',
        tipo_resposta = 'MES',
        criado_por = usuario_admin
    )

    outra_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema2'),
        enunciado = 'enunciado2a',
        tipo_resposta = 'MES',
        criado_por = usuario_admin
    )
    
    nova_pergunta.save()
    outra_pergunta.save()

    Comentario.objects.create(
        pergunta = nova_pergunta,
        email = 'email1@email.com',
        phone = '12345678911',
        is_whatsapp = True,
        mensagem = 'mensagem1'
    )

    Comentario.objects.create(
        pergunta = nova_pergunta,
        email = 'email2@email.com',
        phone = '12345678911',
        is_whatsapp = False,
        mensagem = 'mensagem2'
    )

    return nova_pergunta


@pytest.mark.django_db
def test_administrador_deve_receber_info_de_user_pelo_id(client, usuario_admin):
    test_user = User.objects.create(username='Get user', email='getuser@example.com', password='123456')

    query = querie_usuario.replace('user_id', str(test_user.id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'user': {'id': str(test_user.id), 'username': str(test_user.username), 'email': str(test_user.email), 'pontuacao': 0,'perguntasCriadas': [], 'perguntasRevisadas': [], 'perguntasPublicadas': []}}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_administrador_deve_receber_info_propria_se_user_for_vazio(client, usuario_admin):
    query = usuario_vazio_querie.replace('user_id', str(usuario_admin.id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'user': {'id': str(usuario_admin.id), 'username': str(usuario_admin.username), 'email': str(usuario_admin.email), 'pontuacao': 0, 'perguntasCriadas': [], 'perguntasRevisadas': [], 'perguntasPublicadas': []}}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_admin_deve_listar_todos_usuarios(client, usuario_admin):
    User.objects.create(username='one user', email='oneuser@example.com', password='123456')
    User.objects.create(username='two user', email='twouser@example.com', password='123456')
    User.objects.create(username='three user', email='threeuser@example.com', password='123456')

    query = querie_usuarios

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert resultado == {'data': {'users': [{'id': '4', 'username': 'admin', 'pontuacao': 0}, {'id': '5', 'username': 'one user', 'pontuacao': 0}, {'id': '6', 'username': 'two user', 'pontuacao': 0}, {'id': '7', 'username': 'three user', 'pontuacao': 0}]}}
    assert len(resultado['data']['users']) == len(User.objects.all())
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
def test_deve_retornar_todos_os_comentarios(client, criar_dados_de_teste, usuario_admin, todos_comentarios, todas_perguntas):
    query = todos_comentarios_querie

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'comentarios': [{'id': f'{todos_comentarios[0].id}', 'mensagem': 'mensagem1', 'email': 'email1@email.com', 'phone': '12345678911', 'pergunta': {'id': f'{todas_perguntas[0].id}', 'enunciado': 'enunciado1adadasdasda'}}, {'id': f'{todos_comentarios[1].id}', 'mensagem': 'mensagem2', 'email': 'email2@email.com', 'phone': '12345678911', 'pergunta': {'id': f'{todas_perguntas[0].id}', 'enunciado': 'enunciado1adadasdasda'}}]}}
    assert 'errors' not in resultado

@pytest.mark.parametrize('texto_biblico_referencia', ['te1 1:21', 'te1 1:21-23', 'te1 1:21-23, 2:4', 'te1 1:21-23, 2:4; te2 1:1-3'])
@pytest.mark.django_db
def test_deve_buscar_texto_biblico(client, usuario_admin, criar_dados_de_teste, texto_biblico_referencia):
    query = texto_biblico_querie.replace('texto_biblico_referencia', texto_biblico_referencia)

    print(query)

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    #assert resultado == {'data': {'textoBiblico': [{'livro': {'nome': 'livro1', 'sigla': 'te1', 'testamento': {'nome': 'testamento1'}}, 'versao': {'nome': 'versaonome1', 'sigla': 'VER1'}, 'capitulo': 1, 'versiculo': 21, 'texto': 'Versiculo texto'}]}}
    assert 'errors' not in resultado
    assert 'None' not in resultado


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
    pergunta_mais_nova = Pergunta.objects.last()
    assert resultado == {'data': OrderedDict([('cadastrarPergunta', {'pergunta': {'id': f'{pergunta_mais_nova.id}', 'tema': {'nome': 'tema1'}, 'enunciado': f'{pergunta_mais_nova.enunciado}', 'tipoResposta': f'{pergunta_mais_nova.tipo_resposta}', 'status': pergunta_mais_nova.status, 'revisadoPor': None}})])}
    assert len(Pergunta.objects.all()) == 3
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_editar_nova_pergunta(client, usuario_admin, criar_dados_de_teste):
    nova_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema1'),
        enunciado = 'enunciado1adadasdasda',
        tipo_resposta = 'MES',
        criado_por = usuario_admin,
        status=False
    )
    pergunta_id = nova_pergunta.id

    assert nova_pergunta.enunciado == 'enunciado1adadasdasda'
    assert nova_pergunta.status == False

    tema_id = Tema.objects.get(nome='tema1').id
    referencia_id = Referencia.objects.all()[0].id

    query = editar_pergunta_mutation.replace('tema_id', str(tema_id)).replace('referencia_id', str(referencia_id)).replace('pergunta_id', str(pergunta_id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    nova_pergunta.refresh_from_db()

    assert resultado == {'data': OrderedDict([('editarPergunta', {'pergunta': {'id': f'{nova_pergunta.id}', 'enunciado': 'Novo enunciado', 'revisadoPor': None, 'status': True}})])}
    assert nova_pergunta.enunciado == 'Novo enunciado'
    assert nova_pergunta.status == True
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_adicionar_novo_comentario(client, usuario_admin, criar_dados_de_teste, todas_perguntas):
    pergunta_id = todas_perguntas[0].id
    
    query = adicionar_comentario_mutation.replace('pergunta_id', str(pergunta_id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    comentario_mais_novo = Comentario.objects.last()
    assert resultado == {'data': OrderedDict([('adicionarComentario', {'comentario': {'phone': f'{comentario_mais_novo.phone}', 'isWhatsapp': comentario_mais_novo.is_whatsapp, 'email': f'{comentario_mais_novo.email}', 'mensagem': f'{comentario_mais_novo.mensagem}', 'pergunta': {'id': f'{comentario_mais_novo.pergunta.id}', 'enunciado': f'{comentario_mais_novo.pergunta.enunciado}'}}})])}
    assert len(Comentario.objects.all()) == 3
    assert 'errors' not in resultado