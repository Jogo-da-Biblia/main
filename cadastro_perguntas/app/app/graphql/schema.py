import graphene
from graphene_django import DjangoObjectType

from app.perguntas.models import Pergunta, Tema, Referencia
from app.core.models import User
from django.contrib.auth.models import Group


class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = ("id", "enunciado", "tipo_resposta", "refencia_resposta","status", "revisado_por")


class TemasType(DjangoObjectType):
    class Meta:
        model = Tema
        fields = ("nome", "cor")


class UserTypes(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_active", "is_superuser", "roles")


class Query(graphene.ObjectType):
    perguntas = graphene.List(PerguntasType)
    pergunta = graphene.List(PerguntasType, tema=graphene.String())
    users = graphene.List(UserTypes)
    user = graphene.List(UserTypes, id=graphene.Int())

    def resolve_perguntas(root, info):
        return Pergunta.objects.all()

    def resolve_pergunta(root, info, tema):
        return Pergunta.objects.filter(tema=tema)
    
    def resolve_users(root, info):
        return User.objects.all()

    def resolve_user(root, info, id):
        return User.objects.filter(id=id)

schema = graphene.Schema(query=Query)