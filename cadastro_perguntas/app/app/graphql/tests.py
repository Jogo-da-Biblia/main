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
def perguntas_count():
    return Pergunta.objects.count()

@pytest.fixture
def get_all_perguntas():
    return Pergunta.objects.all()


@pytest.fixture
def delete_all_items():
    Pergunta.objects.all().delete()
    Tema.objects.all().delete()
    Testamento.objects.all().delete()
    Versiculo.objects.all().delete()
    Versao.objects.all().delete()
    Livro.objects.all().delete()
    Referencia.objects.all().delete()


@pytest.fixture
def create_test_data(admin_user, delete_all_items):

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
        criado_por = admin_user
    )

    another_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema2'),
        enunciado = 'enunciado2a',
        tipo_resposta = 'MES',
        criado_por = admin_user
    )
    
    new_pergunta.save()
    another_pergunta.save()
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
def test_should_return_random_pergunta(client, create_test_data, admin_user):
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


@pytest.mark.django_db
def test_should_return_all_perguntas(client, create_test_data, admin_user, get_all_perguntas):
    query = '''
        query{
        perguntas{
            id
            enunciado
        }
    }
    '''

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    
    assert result == {'data': {'perguntas': [{'id': f'{get_all_perguntas[0].id}', 'enunciado': 'enunciado1adadasdasda'}, {'id': f'{get_all_perguntas[1].id}', 'enunciado': 'enunciado2a'}]}}
    assert 'errors' not in result


@pytest.mark.django_db
def test_should_get_texto_biblico(client, admin_user, create_test_data):
    query = '''
        query{
        textoBiblico(
            referencia: "te1 1:21"
            versao: "ver1"
        ){
            textos{
                livro
                livroAbreviado
                versao
                versaoAbreviada
                capitulo
                versiculo
                texto
            }
        }
    }
    '''

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    assert result == {'data': {'textoBiblico': {'textos': [{'livro': 'livro1', 'livroAbreviado': 'te1', 'versao': 'versaonome1', 'versaoAbreviada': 'VER1', 'capitulo': 1, 'versiculo': 21, 'texto': 'Versiculo texto'}]}}}
    assert 'errors' not in result


@pytest.mark.django_db
def test_should_create_new_user(client, admin_user):
    query = '''
        mutation{
        cadastrarUsuario(
            email: "teste1@email.com"
            username: "ususaroteste1"
            isStaff: false
            password: "1938y"
        ){
            user{
            id
            email
            }
        }	
    }
    '''

    result = client.execute(query, context_value=UserInContext(user=admin_user))

    assert User.objects.filter(email='teste1@email.com').exists() == True
    
    new_user = User.objects.get(username='ususaroteste1')

    assert result == {'data': OrderedDict([('cadastrarUsuario', {'user': {'id': str(new_user.id), 'email': str(new_user.email)}})])}
    assert 'errors' not in result


@pytest.mark.django_db
def test_should_edit_new_user(client, admin_user, create_test_data):
    new_user = User.objects.create(email='edit@email.com', username='donoteditthis', is_staff=False)
    user_id = new_user.id

    assert new_user.username == 'donoteditthis'
    assert new_user.email == 'edit@email.com'

    query = '''
        mutation{
        editarUsuario(
            id: user_id
            newUsername:"newusername"
            newEmail: "newemai1l@.com"
        ){
            user{
                id
                username
                email
            }
        }
    }
    '''.replace('user_id', str(user_id))

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    
    assert User.objects.filter(id=user_id).exists() == True

    new_user.refresh_from_db()
    
    assert result == {'data': OrderedDict([('editarUsuario', {'user': {'id': f'{new_user.id}', 'username': 'newusername', 'email': 'newemai1l@.com'}})])}
    assert new_user.username == 'newusername'
    assert new_user.email == 'newemai1l@.com'
    assert 'errors' not in result


@pytest.mark.django_db
def test_should_send_newpassword_email(client, admin_user):
    new_user = User.objects.create(email='user@email.com', username='donoteditthis', is_staff=False)
    user_id = new_user.id

    query = '''
        mutation{
        recuperarSenha(
            userId:user_id, 
            email:"user@email.com"
        ){
            message
        }
    }
    '''.replace('user_id', str(user_id))

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    
    assert result == {'data': OrderedDict([('recuperarSenha', {'message': 'Senha alterada e email enviado com sucesso'})])}
    assert 'errors' not in result


@pytest.mark.django_db
def test_should_add_new_pergunta(client, admin_user, create_test_data):
    tema_id = Tema.objects.get(nome='tema1').id
    referencia_id = Referencia.objects.all()[0].id
    
    query = '''
        mutation{
            cadastrarPergunta(
                enunciado:"Enunciaod da pergunta",
                outrasReferencias: "outras ref",
                referenciaRespostaId: referencia_id,
                temaId: tema_id,
                tipoResposta: "MES",
            ){
                pergunta{
                    id
                    tema{
                        nome
                    }
                    enunciado
                    tipoResposta
                    status
                    revisadoPor {
                        id
                        username
                        email
                    }
                }
            }
        }
    '''.replace('tema_id', str(tema_id)).replace('referencia_id', str(referencia_id))

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    newest_pergunta = Pergunta.objects.last()
    assert result == {'data': OrderedDict([('cadastrarPergunta', {'pergunta': {'id': f'{newest_pergunta.id}', 'tema': {'nome': 'tema1'}, 'enunciado': 'Enunciaod da pergunta', 'tipoResposta': 'MES', 'status': False, 'revisadoPor': None}})])}
    assert len(Pergunta.objects.all()) == 3
    assert 'errors' not in result


@pytest.mark.django_db
def test_should_edit_new_pergunta(client, admin_user, create_test_data):
    new_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='tema1'),
        enunciado = 'enunciado1adadasdasda',
        tipo_resposta = 'MES',
        criado_por = admin_user,
        status=False
    )
    pergunta_id = new_pergunta.id

    assert new_pergunta.enunciado == 'enunciado1adadasdasda'
    assert new_pergunta.status == False

    tema_id = Tema.objects.get(nome='tema1').id
    referencia_id = Referencia.objects.all()[0].id

    query = '''
        mutation{
            editarPergunta(
                id:pergunta_id, 
                enunciado:"Novo enunciado",
                outrasReferencias: "novaOUtraRefe",
                referenciaRespostaId: referencia_id,
                temaId: tema_id,
                tipoResposta: "MES",
                status: true
            ){
                pergunta{
                    id
                    enunciado
                    revisadoPor{
                        id
                        username
                    }
                    status
                    revisadoPor {
                        id
                    }
                }
            }
        }
    '''.replace('tema_id', str(tema_id)).replace('referencia_id', str(referencia_id)).replace('pergunta_id', str(pergunta_id))

    result = client.execute(query, context_value=UserInContext(user=admin_user))
    new_pergunta.refresh_from_db()

    assert result == {'data': OrderedDict([('editarPergunta', {'pergunta': {'id': f'{new_pergunta.id}', 'enunciado': 'Novo enunciado', 'revisadoPor': None, 'status': True}})])}
    assert new_pergunta.enunciado == 'Novo enunciado'
    assert new_pergunta.status == True
    assert 'errors' not in result