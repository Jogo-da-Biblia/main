import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

import pytest
from graphene.test import Client as GrapheneClient
from app.core.models import User
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
    # cria um client do Graphene test
    graphene_client = GrapheneClient(schema)
    return graphene_client


@pytest.mark.django_db
def test_admin_should_get_user_info_by_id(client, admin_user):
    #django_user_model().objects.create_user(d=1, username='Get user', email='getuser@example.com')

    test_user = User.objects.create(username='Get user', email='getuser@example.com', password='123456')
    print(User.objects.all())

    
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
    print(query)

    # graphene_client = Client(schema)
    # graphene_client.force_login(admin_user)
    # graphene_client.context_value  = {'request': admin_client._request(), 'user': admin_user}

    result = client.execute(query, context_value=UserInContext(user=admin_user))

    print(result)
    assert result == {'data': {'user': {'user': {'id': '2', 'username': 'Get user', 'email': 'getuser@example.com'}, 'perguntas': []}}}
    assert 'errors' not in result