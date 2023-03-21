import random

import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField

from app.perguntas.models import Pergunta, Tema, Referencia
from app.core.models import User
from django.contrib.auth.models import Group
from graphene_django.forms.mutation import DjangoModelFormMutation
from app.core.forms import NewUserForm

# utils

def is_user_superuser_or_admin(user):
    if user.is_superuser is False and any([user.groups.filter(name='administradores').exists(), user.groups.filter(name='revisores').exists(), user.groups.filter(name='publicadores').exists()]) is False:
        return False
    return True

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


class UserWithQuestionsType(graphene.ObjectType):
    perguntas = graphene.List(PerguntasType)
    user = graphene.Field(UserType)

    # class Meta:
    #     model = User
    #     fields = ("id", "username", "email", "is_staff", "is_active", "is_superuser")


class Query(graphene.ObjectType):
    perguntas = DjangoListField(PerguntasType)
    pergunta = DjangoListField(PerguntasType, tema=graphene.String())
    users = DjangoListField(UserType)
    user = graphene.Field(UserWithQuestionsType, id=graphene.Int())
    temas = DjangoListField(TemaType)

    # def resolve_perguntas(root, info):
    #     return Pergunta.objects.all()

    def resolve_pergunta(root, info, tema):
        return random.sample(tuple(Pergunta.objects.filter(tema=tema)), 1)
    
    # def resolve_users(root, info):
    #     return User.objects.all()

    def resolve_user(root, info, id=None):
        if info.context.user.id != id:
            if is_user_superuser_or_admin(info.context.user) is False and info.context.user.id != id:
                raise Exception('Somente o proprio usuario ou admins podem ver os dados de outros usuarios')
        
        if id is None:
            user = info.context.user
        else:    
            user = User.objects.get(id=id)

        perguntas = Pergunta.objects.filter(criado_por=User.objects.get(id=user.id))
        return UserWithQuestionsType(perguntas=perguntas, user=user)
    
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
        if is_user_superuser_or_admin(info.context.user) is False:
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
        if is_user_superuser_or_admin(info.context.user) is False and info.context.user.id != id:
            raise Exception('Somente o proprio usuario e administradores podem editar dados de usuarios')
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


class RecuperarSenhaMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)

    user = graphene.Field(UserType)
    
    def mutate(self, info, user_id):
        if is_user_superuser_or_admin(info.context.user) is False and info.context.user.id != user_id:
            raise Exception('Somente o proprio usuario e administradores podem solicitar o envio de nova senha')
        
        user = User.objects.get(id=user_id)

        return RecuperarSenhaMutation(user=user)


# class CadastrarPerguntaMutation(graphene.Mutation):
    
#     class Arguments:
#         tema_id = graphene.Int(required=True)
#         enunciado = graphene.String(required=True)
#         tipo_resposta = graphene.String(required=True)
#         refencia_resposta_id = graphene.Int()
#         outras_referencias = graphene.String()
#         publicado = graphene.Boolean()
    
#     user = graphene.Field(UserType)
    
#     def mutate(self, info, username, email, password, is_staff=False):
#         if is_user_superuser_or_admin(info.context.user) is False:
#             raise Exception('Somente admins podem adicionar novos usuarios')
#         user = User(username=username, email=email, is_staff=is_staff)
#         user.set_password(password)
#         user.save()
#         return CadastrarUsuarioMutation(user=user)

class Mutation(graphene.ObjectType):
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    editar_usuario = EditarUsuarioMutation.Field()
    recuperar_senha = RecuperarSenhaMutation.Field()
    # cadastrarPergunta = CadastrarPerguntaMutation.Field()
    # cadastrar_ou_editar_pergunta = DeletePergunta.Field()




schema = graphene.Schema(query=Query, mutation=Mutation)