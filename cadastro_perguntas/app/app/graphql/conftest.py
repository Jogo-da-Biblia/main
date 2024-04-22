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
from .eg import query_usuario, query_usuarios, pergunta_aleatoria_query, todas_perguntas_query, usuario_vazio_query, texto_biblico_query, novo_usuario_mutation, editar_usuario_mutation, adicionar_nova_pergunta_mutation, editar_pergunta_mutation, reenviar_senha_mutation, todos_comentarios_query, adicionar_comentario_mutation

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
    Tema.objects.create(nome='Conhecimentos Gerais', cor='red')
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
        nome='Galatas',
        sigla='Gl'
    )
    galatas.save()

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
    gl220.save()

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
            livro=mateus,
            capitulo=1,
            versiculo=i,
            texto=f'Versículo de exemplo de Mt 1:{i}'
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


