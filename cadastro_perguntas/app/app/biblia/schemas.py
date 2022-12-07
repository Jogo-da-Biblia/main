# import graphene
from graphene import relay, ObjectType, Schema
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

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
        
        
class Query(ObjectType):
    livro = relay.Node.Field(LivroNode)
    livros = DjangoFilterConnectionField(LivroNode)
    
    testamento = relay.Node.Field(TestamentoNode)
    testamentos = DjangoFilterConnectionField(TestamentoNode)
    
    versiculo = relay.Node.Field(VersiculoNode)
    versiculos = DjangoFilterConnectionField(VersiculoNode)
    
    versao = relay.Node.Field(VersaoNode)
    versoes = DjangoFilterConnectionField(VersaoNode)
    
    
class Mutation(ObjectType):
    pass

schema = Schema(query=Query)

# my_schema = Schema(
#     query=MyRootQuery,
#     mutation=MyRootMutation,
#     subscription=MyRootSubscription
#     types=[SomeExtraObjectType, ]
# )
    