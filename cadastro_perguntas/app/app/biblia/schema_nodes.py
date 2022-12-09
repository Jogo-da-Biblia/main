from graphene import relay, ID, Node
from graphene_django import DjangoObjectType

from .models import Livro, Testamento, Versiculo, Versao

class CustomNode(Node):
    """
        For fetching object id instead of Node id
    """
    class Meta:
        name = 'Nodes'
        
    @staticmethod
    def to_global_id(type, id):
        return id


class LivroNode(DjangoObjectType):
    # id = ID(source='pk', required=True)
    
    class Meta:
        model = Livro
        filter_fields = {
            'nome': ['exact', 'icontains', 'istartswith'],
            'posicao': ['exact', 'icontains'],
            'sigla': ['exact'],
            'testamento': ['exact'],
        }
        interfaces = (CustomNode, )
        
        
    # pk = Int()

    # def resolve_pk(self, info):
    #     return self.pk


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