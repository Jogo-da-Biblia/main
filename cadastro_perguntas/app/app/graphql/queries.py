import graphene
import random
import sys
from django.shortcuts import get_object_or_404

from app.core.utils import (
    check_if_user_is_admin_or_himself,
    usuario_superusuario_ou_admin,
    get_referencia_biblica_from_web,
)
from app.core.models import User
from app.perguntas.models import Pergunta, Tema
from app.comentarios.models import Comentario
from . import types as gql_types
from graphene_django import DjangoListField
from graphql_jwt.decorators import login_required

class Query(graphene.ObjectType):
    perguntas = DjangoListField(
        gql_types.PerguntasType,
        description="Consulta para obter uma lista de todas as perguntas publicadas",
    )

    pergunta = graphene.Field(
        gql_types.PerguntasType,
        id=graphene.Int(),
        description="Consulta para obter uma pergunta específica pelo ID",
    )

    pergunta_aleatoria = graphene.Field(
        gql_types.PerguntasType,
        tema_id=graphene.Int(),
        description="Consulta para obter uma pergunta aleatória publicada. Se um ID de tema for fornecido, filtra pelas perguntas desse tema.",
    )

    users = DjangoListField(
        gql_types.UsuarioType,
        description="Consulta para obter uma lista de todos os usuários",
    )

    user = graphene.Field(
        gql_types.UsuarioType,
        id=graphene.Int(),
        description="Consulta para obter um usuário específico pelo ID. Se nenhum ID for fornecido, retorna o usuário autenticado.",
    )

    temas = DjangoListField(
        gql_types.TemaType,
        description="Consulta para obter uma lista de todos os temas",
    )

    tema = graphene.Field(
        gql_types.TemaType,
        id=graphene.Int(),
        description="Consulta para obter um tema específico pelo ID",
    )

    comentarios = DjangoListField(
        gql_types.ComentariosType,
        description="Consulta para obter uma lista de todos os comentários",
    )

    referencia = graphene.List(
        gql_types.ReferenciaType,
        referencia=graphene.String(),
        description="Consulta para obter uma lista de referências bíblicas com base em uma string de referência fornecida",
    )

    @login_required
    def resolve_pergunta_aleatoria(root, info, tema_id=None):
        if tema_id is None:
            try:
                random_pergunta_id = random.choice(
                    Pergunta.objects.filter(publicado_status=True).values_list(
                        "id", flat=True
                    )
                )
            except IndexError:
                raise Exception("Nenhuma pergunta publicada foi encontrada")
        else:
            tema = get_object_or_404(Tema, id=tema_id)
            try:
                random_pergunta_id = random.choice(
                    Pergunta.objects.filter(
                        tema=tema, publicado_status=True
                    ).values_list("id", flat=True)
                )
            except IndexError:
                raise Exception(
                    "Nenhuma pergunta publicada foi encontrada com o tema escolhido"
                )

        return Pergunta.objects.get(id=random_pergunta_id)

    @login_required
    def resolve_pergunta(root, info, id):
        return Pergunta.objects.get(id=id)

    @login_required
    def resolve_perguntas(root, info):
        return Pergunta.objects.all()

    @login_required
    def resolve_user(root, info, id=None):
        user_id = info.context.user.id if id is None else id

        assert check_if_user_is_admin_or_himself(info, user_id)

        return User.objects.get(id=user_id)

    @login_required
    def resolve_users(root, info):
        assert usuario_superusuario_ou_admin(info.context.user, raise_exception=True)

        return User.objects.all()

    @login_required
    def resolve_comentarios(root, info):
        return Comentario.objects.all()

    @login_required
    def resolve_temas(root, info):
        print(info.context.user, file=sys.stderr)
        return Tema.objects.all()

    @login_required
    def resolve_tema(root, info, id):
        return Tema.objects.get(id=id)

    @login_required
    def resolve_referencia(root, info, referencia):
        all_referencias = get_referencia_biblica_from_web(referencia)
        return [gql_types.ReferenciaType(**ref) for ref in all_referencias]
