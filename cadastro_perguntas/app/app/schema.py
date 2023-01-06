import graphene
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField

from app.biblia.schema_nodes import *
from app.biblia.models import *

from app.perguntas.schema_nodes import *
from app.perguntas.mutations import *
from app.perguntas.models import *

from django.contrib.auth import get_user_model
from app.core.schema_nodes import UserType


User = get_user_model()

class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return User.objects.all()
    
    me = graphene.Field(UserType)
    
    def resolve_me(root, info):
        try:
            user = User.objects.get(pk=info.context.user.pk)
            return user
        except Exception:
            return None
        
    user = graphene.Field(UserType, id=graphene.Int())
    
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
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
