import graphene as g
from graphene_django import DjangoObjectType

from .models import Livro, Testamento, Versiculo, Versao

class CustomNode(g.Node):
    """
        For fetching object id instead of Node id
    """
    class Meta:
        name = 'NodeId'
        
    @staticmethod
    def to_global_id(type, id):
        return id


class LivroNode(DjangoObjectType):
    # id = g.ID(source='pk', required=True)
    
    class Meta:
        model = Livro
        filter_fields = {
            'nome': ['exact', 'icontains', 'istartswith'],
            'posicao': ['exact', 'icontains'],
            'sigla': ['exact'],
            'testamento': ['exact'],
        }
        interfaces = (CustomNode, )


class TestamentoNode(DjangoObjectType):
    class Meta:
        model = Testamento
        filter_fields = ["nome"]
        fields = "__all__"
        interfaces = (CustomNode, )


class VersiculoNode(DjangoObjectType):
    class Meta:
        model = Versiculo
        filter_fields = {
            'livro': ['exact'],
            'capitulo': ['exact'],
            'versiculo': ['exact'],
        }
        interfaces = (CustomNode, )
        fields = "__all__"


class VersaoNode(DjangoObjectType):
    class Meta:
        model = Versao
        filter_fields = ["nome"]
        fields = "__all__"
        interfaces = (CustomNode, )
        
        