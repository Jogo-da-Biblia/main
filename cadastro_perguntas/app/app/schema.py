import graphene
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField

import app.biblia.schema as biblia
from app.biblia.models import *

from app.perguntas.schema import *
from app.perguntas.mutations import *
from app.perguntas.models import *

from django.contrib.auth import get_user_model
import app.core.schema as core


User = get_user_model()

class Query(graphene.ObjectType):
    users = graphene.List(core.UserType)

    def resolve_users(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return User.objects.all()
    
    me = graphene.Field(core.UserType)
    
    def resolve_me(root, info):
        try:
            user = User.objects.get(pk=info.context.user.pk)
            return user
        except Exception:
            return None
        
    user = graphene.Field(core.UserType, id=graphene.Int())
    
    def resolve_user(root, info, id):
        try:
            user = User.objects.get(id=id)
            return user
        except Exception:
            return None
    
    livro = graphene.Field(biblia.LivroNode, id=graphene.Int())
    livros = DjangoFilterConnectionField(biblia.LivroNode)

    def resolve_livro(root, info, id):
        try:
            livro = Livro.objects.get(id=id)
            return livro
        except Exception:
            return None
    
    testamento = graphene.relay.Node.Field(biblia.TestamentoNode)
    testamentos = DjangoFilterConnectionField(biblia.TestamentoNode)
    
    versiculo = graphene.relay.Node.Field(biblia.VersiculoNode)
    versiculos = DjangoFilterConnectionField(biblia.VersiculoNode)
    
    versao = graphene.relay.Node.Field(biblia.VersaoNode)
    versoes = DjangoFilterConnectionField(biblia.VersaoNode)
    
    tema = graphene.relay.Node.Field(TemaNode)
    
    temas = graphene.List(TemaNode)
    
    def resolve_temas(root, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return Tema.objects.all()
    
    referencia = graphene.relay.Node.Field(ReferenciaNode)
    referencias = DjangoFilterConnectionField(ReferenciaNode)
    
    pergunta = graphene.relay.Node.Field(PerguntaNode)
    perguntas = DjangoFilterConnectionField(PerguntaNode)
    
    alternativa = graphene.relay.Node.Field(AlternativaNode)
    alternativas = g.List(AlternativaNode)
    
    
class Mutation(core.Mutation, graphene.ObjectType):
    create_tema = CreateTema.Field()
    create_referencia = CreateReferencia.Field()
    create_pergunta = CreatePergunta.Field()
    create_alternativa = CreateAlternativa.Field()
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
