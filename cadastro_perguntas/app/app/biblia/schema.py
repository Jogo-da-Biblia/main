# import graphene
from graphene import relay, ObjectType, Schema, Mutation
from graphene_django.filter import DjangoFilterConnectionField
from .schema_nodes import *
from .mutations import *
        
        
class Query(ObjectType):
    nodes = relay.Node.Field()
    
    livro = relay.Node.Field(LivroNode)
    livros = DjangoFilterConnectionField(LivroNode)
    
    testamento = relay.Node.Field(TestamentoNode)
    testamentos = DjangoFilterConnectionField(TestamentoNode)
    
    versiculo = relay.Node.Field(VersiculoNode)
    versiculos = DjangoFilterConnectionField(VersiculoNode)
    
    versao = relay.Node.Field(VersaoNode)
    versoes = DjangoFilterConnectionField(VersaoNode)
    
    
class Mutation(ObjectType):
    create_livro = CreateLivroMutation.Field()
    update_livro = UpdateLivroMutation.Field()
    # delete_livro
    
    create_testamento = CreateTestamentoMutation.Field()
    # update_testamento
    # delete_testamento
    
    create_versiculo = CreateVersiculoMutation.Field()
    # update_versiculo
    # delete_versiculo
    
    create_versao = CreateVersaoMutation.Field()
    # update_versao
    # delete_versao
    

biblia_schema = Schema(query=Query, mutation=Mutation)

# my_schema = Schema(
#     query=MyRootQuery,
#     mutation=MyRootMutation,
#     subscription=MyRootSubscription
#     types=[SomeExtraObjectType, ]
# )
    