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
from .test_queries import query_usuario, query_usuarios, pergunta_aleatoria_query, todas_perguntas_query, usuario_vazio_query, texto_biblico_query, novo_usuario_mutation, editar_usuario_mutation, adicionar_nova_pergunta_mutation, editar_pergunta_mutation, reenviar_senha_mutation, todos_comentarios_query, adicionar_comentario_mutation

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
    Tema.objects.create(nome='Conhecimentos Gerais', cor='vermelho')
    Tema.objects.create(nome='Doutrina', cor='roxo')

    nt = Testamento(nome='Novo Testamento')
    nt.save()
    
    genesis = Livro(
        testamento=Testamento.objects.create(nome='Antigo Testamento'),
        posicao=1,
        nome='Gênesis',
        sigla='Gn'
    )
    genesis.save()

    mateus = Livro(
        testamento=nt,
        posicao=1,
        nome='Mateus',
        sigla='Mt'
    )
    mateus.save()

    galatas = Livro(
        testamento=nt,
        posicao=1,
        nome='Mateus',
        sigla='Mt'
    )
    mateus.save()

    ara = Versao(nome='Almeida Revista e Atualizada', sigla='ARA')
    ara.save()

    gn126 = Versiculo(
        versao=ara,
        livro=genesis,
        capitulo=1,
        versiculo=26,
        texto='Também disse Deus: Façamos o homem à nossa imagem, conforme a nossa semelhança; tenha ele domínio sobre os peixes do mar, sobre as aves dos céus, sobre os animais domésticos, sobre toda a terra e sobre todos os répteis que rastejam pela terra.'
    )
    gn126.save()

    gl220 = Versiculo(
        versao=ara,
        livro=galatas,
        capitulo=2,
        versiculo=20,
        texto='Já estou crucificado com Cristo; e vivo, não mais eu, mas Cristo vive em mim; e a vida que agora vivo na carne, vivo-a na fé no filho de Deus, o qual me amou, e se entregou a si mesmo por mim.'
    )
    gn126.save()

    # Criando 3 versículos mais de cada livro
    for i in range(1,4):
        Versiculo.objects.create(
            versao=ara,
            livro=genesis,
            capitulo=1,
            versiculo=26+i,
            texto=f'Versículo de exemplo de Gn 1:{26+i}'
        )
        Versiculo.objects.create(
            versao=ara,
            livro=mateus,
            capitulo=28,
            versiculo=i,
            texto=f'Versículo de exemplo de Mt 28:{i}'
        )

    Versiculo.objects.create(
        versao=ara,
        livro=genesis,
        capitulo=2,
        versiculo=1,
        texto='Assim foram acabados os céus e a terra, com todo o seu exército.'
        )
    
    Versiculo.objects.create(
        versao=ara,
        livro=genesis,
        capitulo=1,
        versiculo=31,
        texto='E viu Deus tudo quanto fizera, e eis que era muito bom. E foi a tarde e a manhã, o dia sexto.'
        )

    Referencia.objects.create(
        livro=genesis,
        versiculo=gn126
    )

    pergunta1 = Pergunta.objects.create(
        tema = Tema.objects.get(nome='Conhecimentos Gerais'),
        enunciado = 'Quem criou o homem?',
        tipo_resposta = 'MES',
        criado_por = usuario_admin
    )

    pergunta2 = Pergunta.objects.create(
        tema = Tema.objects.get(nome='Doutrina'),
        enunciado = 'O que Jesus nos mandou fazer?',
        tipo_resposta = 'MES',
        criado_por = usuario_admin
    )
    
    pergunta1.save()
    pergunta2.save()

    Comentario.objects.create(
        pergunta = pergunta1,
        email = 'comentarista1@email.com',
        phone = '71992540723',
        is_whatsapp = True,
        mensagem = 'Aqui vai o primeiro comentário'
    )

    Comentario.objects.create(
        pergunta = pergunta2,
        email = 'comentarista2@email.com',
        phone = '12345678911',
        is_whatsapp = False,
        mensagem = 'Aqui vai o segundo comentário'
    )

    return pergunta2


@pytest.mark.django_db
def test_administrador_deve_receber_info_de_user_pelo_id(client, usuario_admin):
    usuario_de_teste = User.objects.create(username='user1', email='getuser@example.com', password='123456')

    query = query_usuario.replace('user_id', str(usuario_de_teste.id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'user': {'id': str(usuario_de_teste.id), 'username': str(usuario_de_teste.username), 'email': str(usuario_de_teste.email), 'pontuacao': 0,'perguntasCriadas': [], 'perguntasRevisadas': [], 'perguntasPublicadas': []}}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_administrador_deve_receber_info_propria_se_user_for_vazio(client, usuario_admin):
    query = usuario_vazio_query.replace('user_id', str(usuario_admin.id))

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'user': {'id': str(usuario_admin.id), 'username': str(usuario_admin.username), 'email': str(usuario_admin.email), 'pontuacao': 0, 'perguntasCriadas': [], 'perguntasRevisadas': [], 'perguntasPublicadas': []}}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_admin_deve_listar_todos_usuarios(client, usuario_admin):
    User.objects.create(username='user5', email='oneuser@example.com', password='123456')
    User.objects.create(username='user6', email='twouser@example.com', password='123456')
    User.objects.create(username='user7', email='threeuser@example.com', password='123456')

    query = query_usuarios

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert resultado == {'data': {'users': [{'id': '4', 'username': 'admin', 'pontuacao': 0}, {'id': '5', 'username': 'user5', 'pontuacao': 0}, {'id': '6', 'username': 'user6', 'pontuacao': 0}, {'id': '7', 'username': 'user7', 'pontuacao': 0}]}}
    assert len(resultado['data']['users']) == len(User.objects.all())
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_retornar_pergunta_aleatoria(client, criar_dados_de_teste, usuario_admin):
    query = pergunta_aleatoria_query

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'pergunta': [{'id': '1', 'enunciado': 'enunciado1adadasdasda'}]}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_retornar_todas_as_perguntas(client, criar_dados_de_teste, usuario_admin, todas_perguntas):
    query = todas_perguntas_query

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    
    assert resultado == {'data': {'perguntas': [{'id': f'{todas_perguntas[0].id}', 'enunciado': 'enunciado1adadasdasda'}, {'id': f'{todas_perguntas[1].id}', 'enunciado': 'enunciado2a'}]}}
    assert 'errors' not in resultado

@pytest.mark.django_db
def test_deve_retornar_todos_os_comentarios(client, criar_dados_de_teste, usuario_admin, todos_comentarios, todas_perguntas):
    query = todos_comentarios_query

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
    assert resultado == {'data': {'comentarios': [{'id': f'{todos_comentarios[0].id}', 'mensagem': 'mensagem1', 'email': 'email1@email.com', 'phone': '12345678911', 'pergunta': {'id': f'{todas_perguntas[0].id}', 'enunciado': 'enunciado1adadasdasda'}}, {'id': f'{todos_comentarios[1].id}', 'mensagem': 'mensagem2', 'email': 'email2@email.com', 'phone': '12345678911', 'pergunta': {'id': f'{todas_perguntas[0].id}', 'enunciado': 'enunciado1adadasdasda'}}]}}
    assert 'errors' not in resultado

@pytest.mark.parametrize('texto_biblico_referencia', ['Gn 1:26', 'Gn 1:26-28', 'Gn 1:26,28', 'Gn 1:26-28,31', 'Gn 1:27-29, 2:1', 'Gn 1:27,28,31, 2:1', 'Gn 1:26-28,31, 2:1; Mt 1:1-3', 'Gn 1:26-28,31,2:1; Mt 1:1,2, 1:3', 'Gn 1:26-28,31, 2:1; Mt 1:1-3; Gl 2:20'])
@pytest.mark.django_db
def test_deve_buscar_texto_biblico(client, usuario_admin, criar_dados_de_teste, texto_biblico_referencia):
    query = texto_biblico_query.replace('texto_biblico_referencia', texto_biblico_referencia)

    print(query)

    resultado = client.execute(query, context_value=UsuarioEmContexto(usuario=usuario_admin))
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