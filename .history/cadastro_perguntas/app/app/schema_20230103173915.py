import graphene
from graphene_django.filter import DjangoFilterConnectionField

from app.biblia.schema_nodes import *
from app.biblia.models import *

from app.perguntas.schema_nodes import *
from app.perguntas.mutations import *
from app.perguntas.models import *

from django.contrib.auth import get_user_model
from app.core.schema_nodes import UserNode

User = get_user_model()


class Query(graphene.ObjectType):
    user = graphene.Field(UserNode, id=graphene.Int())
    
    def resolve_user(root, info, id):
        try:
            user = User.objects.get(id=id)
            return user
        except Exception:
            return None
    
    livro = graphene.Field(LivroNode, id=graphene.Int())
    livros = DjangoFilterConnectionField(LivroNode)

    def resolve_livro(root, info, id):
        try:
            livro = Livro.objects.get(id=id)
            return livro
        except Exception:
            return None
    
    testamento = graphene.relay.Node.Field(TestamentoNode)
    testamentos = DjangoFilterConnectionField(TestamentoNode)
    
    versiculo = graphene.relay.Node.Field(VersiculoNode)
    versiculos = DjangoFilterConnectionField(VersiculoNode)
    
    versao = graphene.relay.Node.Field(VersaoNode)
    versoes = DjangoFilterConnectionField(VersaoNode)
    
    tema = graphene.relay.Node.Field(TemaNode)
    temas = DjangoFilterConnectionField(TemaNode)
    
    referencia = graphene.relay.Node.Field(ReferenciaNode)
    referencias = DjangoFilterConnectionField(ReferenciaNode)
    
    pergunta = graphene.relay.Node.Field(PerguntaNode)
    perguntas = DjangoFilterConnectionField(PerguntaNode)
    
    alternativa = graphene.relay.Node.Field(AlternativaNode)
    alternativas = g.List(AlternativaNode)
    
    
class Mutation(graphene.ObjectType):
    create_tema = CreateTema.Field()
    create_referencia = CreateReferencia.Field()
    create_pergunta = CreatePergunta.Field()
    create_alternativa = CreateAlternativa.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

# my_schema = Schema(
#     query=MyRootQuery,
#     mutation=MyRootMutation,
#     subscription=MyRootSubscription
#     types=[SomeExtraObjectType, ]
# )