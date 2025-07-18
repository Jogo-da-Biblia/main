import os

import django
import pytest
from app.comentarios.models import Comentario
from app.core.models import User
from app.perguntas.models import Pergunta, Tema
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from graphene_django.utils.testing import graphql_query
from model_bakery import baker
from collections import namedtuple
from unittest.mock import Mock

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()


# Usuario enviado no context graphql
class UsuarioEmContexto:
    def __init__(self, usuario):
        self.user = usuario


@pytest.fixture
def usuario_superuser(db):
    try:
        usuario = User.objects.get(username="admin")
    except ObjectDoesNotExist:
        usuario = User.objects.create_superuser(
            username="admin", password="admin", email="admin@admin.com"
        )
    return usuario


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
    Comentario.objects.all().delete()


@pytest.fixture
def criar_dados_de_teste(usuario_superuser, delete_todos_items, db):
    Tema.objects.create(nome="Conhecimentos Gerais", cor="red")
    Tema.objects.create(nome="Doutrina", cor="roxo")

    pergunta1 = Pergunta.objects.create(
        tema=Tema.objects.get(nome="Conhecimentos Gerais"),
        enunciado="Quem criou o homem?",
        tipo_resposta="MES",
        criado_por=usuario_superuser,
    )

    pergunta2 = Pergunta.objects.create(
        tema=Tema.objects.get(nome="Doutrina"),
        enunciado="O que Jesus nos mandou fazer?",
        tipo_resposta="MES",
        criado_por=usuario_superuser,
    )

    pergunta1.save()
    pergunta2.save()

    Comentario.objects.create(
        pergunta=pergunta1,
        email="comentarista1@email.com",
        phone="71992540723",
        is_whatsapp=True,
        mensagem="Aqui vai o primeiro comentário",
    )

    Comentario.objects.create(
        pergunta=pergunta2,
        email="comentarista2@email.com",
        phone="12345678911",
        is_whatsapp=False,
        mensagem="Aqui vai o segundo comentário",
    )

    return pergunta2


@pytest.fixture
def admin_group():
    return Group.objects.get_or_create(name="administradores")[0]


@pytest.fixture
def revisor_group():
    return Group.objects.get_or_create(name="revisores")[0]


@pytest.fixture
def publicador_group():
    return Group.objects.get_or_create(name="publicadores")[0]


@pytest.fixture
def colaborador_group():
    return Group.objects.get_or_create(name="colaboradores")[0]


@pytest.fixture
def admin_user(admin_group):
    user = baker.make("core.User", _fill_optional=True)
    admin_group, _ = Group.objects.get_or_create(name="administradores")
    user.groups.add(admin_group)
    return user


@pytest.fixture
def revisor_user(revisor_group):
    user = baker.make("core.User", _fill_optional=True)
    user.groups.add(revisor_group)
    return user


@pytest.fixture
def publicador_user(publicador_group):
    user = baker.make("core.User", _fill_optional=True)
    user.groups.add(publicador_group)
    return user


@pytest.fixture
def user(colaborador_group):
    user = baker.make("core.User", _fill_optional=True)
    user.groups.add(colaborador_group)
    return user


@pytest.fixture
def admin_client_with_login(client, admin_user):
    client.force_login(admin_user)
    return client


@pytest.fixture
def staff_client_graphql(staff_client_with_login):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=staff_client_with_login)

    return func


@pytest.fixture
def client_with_login(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def client_graphql_with_login(client_with_login):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client_with_login)

    return func


@pytest.fixture
def client_graphql_without_login(client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=client)

    return func


@pytest.fixture
def mocker_request_get(mocker):
    mock_response_data = [
        {
            "versao_abrev": "ARA",
            "livro_abrev": "Jo",
            "capitulo": 3,
            "versiculo": 16,
            "texto": "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna.",
        },
        {
            "versao_abrev": "ARA",
            "livro_abrev": "Jo",
            "capitulo": 3,
            "versiculo": 17,
            "texto": "Porque Deus enviou o seu Filho ao mundo, não para que julgasse o mundo, mas para que o mundo fosse salvo por ele.",
        },
        {
            "versao_abrev": "ARA",
            "livro_abrev": "Jo",
            "capitulo": 3,
            "versiculo": 18,
            "texto": "Quem crê nele não é julgado; mas quem não crê, já está julgado; porquanto não crê no nome do unigênito Filho de Deus.",
        },
    ]
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_data
    return mocker.patch("requests.get", return_value=mock_response)


@pytest.fixture
def mocker_request_get_error(mocker):
    Response = namedtuple("Response", ["status_code"])
    return mocker.patch("requests.get", return_value=Response(status_code=500))
