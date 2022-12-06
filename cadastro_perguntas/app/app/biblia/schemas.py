from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Livro, Testamento, Versiculo, Versao


class LivroNode(DjangoObjectType):
    class Meta:
        model = Livro
        fields = "__all__"
        filter_fields = ["nome", "posicao", "sigla", "testamento"]
        # filter_fields = {
        #     'nome': ['exact', 'icontains', 'istartswith'],
        #     'posicao': ['exact', 'icontains'],
        #     'sigla': ['exact'],
        #     'testamento': ['exact'],
        #     'testamento__name': ['exact'],
        # }
        interfaces = (relay.Node, )


class TestamentoNode(DjangoObjectType):
    class Meta:
        model = Testamento
        fields = "__all__"
        interfaces = (relay.Node, )


class VersiculoNode(DjangoObjectType):
    class Meta:
        model = Versiculo
        fields = "__all__"
        interfaces = (relay.Node, )


class VersaoNode(DjangoObjectType):
    class Meta:
        model = Versao
        fields = "__all__"
        interfaces = (relay.Node, )
        
        
# Connections------------------------------------------
class LivroConnection(relay.Connection):
    class Meta:
        node = LivroNode
        
        
class TestamentoConnection(relay.Connection):
    class Meta:
        node = TestamentoNode
        
        
class VersiculoConnection(relay.Connection):
    class Meta:
        node = VersiculoNode
        
        
class VersaoConnection(relay.Connection):
    class Meta:
        node = VersaoNode


class Query(ObjectType):
    livro = relay.Node.Field(LivroNode)
    livros = DjangoFilterConnectionField(LivroNode)
    
    testamento = relay.Node.Field(TestamentoNode)
    testamentos = relay.ConnectionField(TestamentoConnection)
    
    versiculo = relay.Node.Field(VersiculoNode)
    versiculos = relay.ConnectionField(VersiculoConnection)
    
    versao = relay.Node.Field(VersaoNode)
    versoes = relay.ConnectionField(VersaoConnection)
    
    
class Mutation(ObjectType):
    pass

# schema = graphene.Schema(query=Query, mutation=Mutation)
    