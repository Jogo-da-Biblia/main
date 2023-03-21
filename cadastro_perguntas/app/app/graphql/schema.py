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
        is_staff = graphene.Boolean()
    
    user = graphene.Field(UserType)
    
    def mutate(self, info, username, email, password, is_staff=False):
        if info.context.user.is_superuser is False:
            raise Exception('Somente admins podem adicionar novos usuarios')
        user = User(username=username, email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()
        return CadastrarUsuarioMutation(user=user)


class EditarUsuarioMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        new_username = graphene.String()
        new_email = graphene.String()
        new_password = graphene.String()
        new_is_staff = graphene.Boolean()
    
    user = graphene.Field(UserType)
    
    def mutate(self, info, id, new_username=None, new_email=None, new_password=None, new_is_staff=None):
        if info.context.user.is_superuser is False and info.context.user.id != id:
            raise Exception('Somente o proprio usuario e admins podem editar dados de usuarios')
        user = User.objects.get(id=id)

        if new_username is not None:
            user.username = new_username
        if new_email is not None:
            user.email = new_email
        if new_password is not None:
            user.set_password(new_password)
        
        if info.context.user.is_superuser:
            if new_is_staff is not None:
                user.is_staff = new_is_staff
        user.save()
        return EditarUsuarioMutation(user=user)


class Mutation(graphene.ObjectType):
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    editar_usuario = EditarUsuarioMutation.Field()
    #recuperar_senha = UpdatePergunta.Field()
    #cadastrar_ou_editar_pergunta = DeletePergunta.Field()




schema = graphene.Schema(query=Query, mutation=Mutation)