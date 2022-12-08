from graphene import relay
from graphene_django import DjangoObjectType

from .models import Livro, Testamento, Versiculo, Versao


class LivroNode(DjangoObjectType):
    class Meta:
        model = Livro
        filter_fields = {
            'nome': ['exact', 'icontains', 'istartswith'],
            'posicao': ['exact', 'icontains'],
            'sigla': ['exact'],
            'testamento': ['exact'],
        }
        interfaces = (relay.Node, )


class TestamentoNode(DjangoObjectType):
    class Meta:
        model = Testamento
        filter_fields = ["nome"]
        fields = "__all__"
        interfaces = (relay.Node, )


class VersiculoNode(DjangoObjectType):
    class Meta:
        model = Versiculo
        filter_fields = ["livro"]
        interfaces = (relay.Node, )
        fields = "__all__"


class VersaoNode(DjangoObjectType):
    class Meta:
        model = Versao
        filter_fields = ["nome"]
        fields = "__all__"
        interfaces = (relay.Node, )