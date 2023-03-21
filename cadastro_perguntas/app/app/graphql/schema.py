import random

import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField

from app.perguntas.models import Pergunta, Tema, Referencia
from app.core.models import User
from django.contrib.auth.models import Group
from graphene_django.forms.mutation import DjangoModelFormMutation
from app.core.forms import NewUserForm

# Queries

class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = ("id", "enunciado", "tipo_resposta", "refencia_resposta","status", "revisado_por", "tema")


class TemaType(DjangoObjectType):
    class Meta:
        model = Tema
        fields = ("nome", "cor")


class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_active", "is_superuser")


class Query(graphene.ObjectType):
    perguntas = DjangoListField(PerguntasType)
    pergunta = DjangoListField(PerguntasType, tema=graphene.String())
    users = DjangoListField(UserType)
    user = DjangoListField(UserType, id=graphene.Int())
    temas = DjangoListField(TemaType)

    # def resolve_perguntas(root, info):
    #     return Pergunta.objects.all()

    def resolve_pergunta(root, info, tema):
        return random.sample(tuple(Pergunta.objects.filter(tema=tema)), 1)
    
    # def resolve_users(root, info):
    #     return User.objects.all()

    def resolve_user(root, info, id):
        return User.objects.filter(id=id)
    
    # def resolve_temas(root, info):
    #     return Tema.objects.all()


# # Mutations


class CadastrarUsuarioMutation(graphene.Mutation):
    
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        is_staff = graphene.Boolean(required=True)
    
    user = graphene.Field(UserType)
    
    def mutate(self, info, username, email, password, is_staff):
        if info.context.user.is_superuser is False:
            raise Exception('Somente admins podem adicionar novos usuarios')
        user = User(username=username, email=email, is_staff=is_staff, password=password)
        user.save()
        return CadastrarUsuarioMutation(user=user)


class Mutation(graphene.ObjectType):
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    #editar_usuario = EditarUsuarioMutation.Field()
    #recuperar_senha = UpdatePergunta.Field()
    #cadastrar_ou_editar_pergunta = DeletePergunta.Field()




schema = graphene.Schema(query=Query, mutation=Mutation)