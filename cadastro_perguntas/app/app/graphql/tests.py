import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

import pytest
from graphene.test import Client as GrapheneClient
from app.core.models import User
from app.biblia.models import Livro, Versiculo, Testamento, Versao
from app.perguntas.models import Pergunta, Tema, Referencia
from django.core.exceptions import ObjectDoesNotExist
from .schema import schema


class UserInContext:
    def __init__(self, user):
        self.user = user


@pytest.fixture
def admin_user():
    try:
        user = User.objects.get(username='admin')
    except ObjectDoesNotExist:
        user = User.objects.create_superuser(username='admin', password='admin', email='admin@admin.com')
    return user

@pytest.fixture
def client():
    graphene_client = GrapheneClient(schema)
    return graphene_client


@pytest.fixture
def new_pergunta(admin_user):
    Tema.objects.create(nome='tema1', cor='rosa')
    Tema.objects.create(nome='tema2', cor='dois')

    test_livro = Livro(
        testamento=Testamento.objects.create(nome='testamento1'),
        posicao=1,
        nome='livro1',
        sigla='123'
    )
    test_livro.save()

    # test_referencia = Referencia.objects.create(
    #     livro=test_livro, 
    #     versiculo=Versiculo.objects.create(
    #         versao = Versao.objects.create(nome='versao1', sigla='123'),
    #         livro = test_livro,
    #         capitulo=2,
    #         versiculo=1,
    #         texto='texto1'
    #     )
    # )
    # test_referencia.save()

    new_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema1'),
        enunciado = 'enunciado1adadasdasda',
        tipo_resposta = 'MES',
        criado_por = admin_user
    )
    new_pergunta.save()
    return new_pergunta

@pytest.mark.django_db
def test_admin_should_get_user_info_by_id(client, admin_user):
    test_user = User.objects.create(username='Get user', email='getuser@example.com', password='123456')

    query = '''
        query{
            user(id:user_id){
                user{
                    id
                    username
                    email
                }
                perguntas {
                    id
                    enunciado
                    status
                }
            }
        }
    '''.replace('user_id', str(test_user.id))

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    assert result == {'data': {'user': {'user': {'id': str(test_user.id), 'username': str(test_user.username), 'email': str(test_user.email)}, 'perguntas': []}}}
    assert 'errors' not in result


@pytest.mark.django_db
def test_admin_should_get_own_user_info_if_user_is_null(client, admin_user):
    query = '''
        query{
            user{
                user{
                    id
                    username
                    email
                }
                perguntas {
                    id
                    enunciado
                    status
                }
            }
        }
    '''.replace('user_id', str(admin_user.id))

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    assert result == {'data': {'user': {'user': {'id': str(admin_user.id), 'username': str(admin_user.username), 'email': str(admin_user.email)}, 'perguntas': []}}}
    assert 'errors' not in result


@pytest.mark.django_db
def test_admin_should_list_all_users(client, admin_user):
    User.objects.create(username='one user', email='oneuser@example.com', password='123456')
    User.objects.create(username='two user', email='twouser@example.com', password='123456')
    User.objects.create(username='three user', email='threeuser@example.com', password='123456')

    query = '''
        query{
            users{
                user{
                    id
                    username
                    score
                }
        }
    }
    '''

    result = client.execute(query, context_value=UserInContext(user=admin_user))

    assert result == {'data': {'users': {'user': [{'id': '4', 'username': 'admin', 'score': 0}, {'id': '5', 'username': 'one user', 'score': 0}, {'id': '6', 'username': 'two user', 'score': 0}, {'id': '7', 'username': 'three user', 'score': 0}]}}}
    assert len(result['data']['users']['user']) == len(User.objects.all())
    assert 'errors' not in result


@pytest.mark.django_db
def test_should_return_random_pergunta(client, new_pergunta):

    query = '''
        query{
        pergunta(temaId:1){
            id
            enunciado
        }
    }
    '''

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    assert result == {'data': {'pergunta': [{'id': '1', 'enunciado': 'enunciado1adadasdasda'}]}}
    assert 'errors' not in result