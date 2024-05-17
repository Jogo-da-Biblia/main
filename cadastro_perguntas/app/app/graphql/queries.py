import graphene
import random
from django.shortcuts import get_object_or_404

from app.core.utils import (
    check_if_user_is_admin_or_himself,
    usuario_superusuario_ou_admin,
)
from app.core.models import User
from app.perguntas.models import Pergunta, Tema
from app.comentarios.models import Comentario
from . import types as gql_types
from graphene_django import DjangoListField
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    perguntas = DjangoListField(gql_types.PerguntasType)
    pergunta = graphene.Field(gql_types.PerguntasType, id=graphene.Int())
    pergunta_aleatoria = graphene.Field(gql_types.PerguntasType, tema_id=graphene.Int())
    users = DjangoListField(gql_types.UsuarioType)
    user = graphene.Field(gql_types.UsuarioType, id=graphene.Int())
    comentarios = DjangoListField(gql_types.ComentariosType)
    # TODO Adicionar uma migration para selecionar comentarios de uma pergunta
    temas = DjangoListField(gql_types.TemaType)

    @login_required
    def resolve_pergunta_aleatoria(root, info, tema_id):
        tema = get_object_or_404(Tema, id=tema_id)
        return random.choice(tuple(Pergunta.objects.filter(tema=tema).all()))

    @login_required
    def resolve_pergunta(root, info, id):
        return Pergunta.objects.get(id=id)

    @login_required
    def resolve_perguntas(root, info):
        return Pergunta.objects.all()

    @login_required
    def resolve_user(root, info, id=None):
        assert check_if_user_is_admin_or_himself(info, id)

        if id is None:
            return info.context.user
        return User.objects.get(id=id)


    @login_required
    def resolve_users(root, info):
        assert usuario_superusuario_ou_admin(info.context.user, raise_exception=True)

        return User.objects.all()

    @login_required
    def resolve_comentarios(root, info):
        return Comentario.objects.all()

    @login_required
    def resolve_temas(root, info):
        return Tema.objects.all()
