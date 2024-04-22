import graphene
import random
from app.core.models import User
from app.perguntas.models import Pergunta, Tema
from . import types as gql_types
from graphene_django import DjangoListField


"""
========== Queries ==========
"""

class Query(graphene.ObjectType):
    perguntas = DjangoListField(gql_types.PerguntasType)
    pergunta = DjangoListField(gql_types.PerguntasType, tema_id=graphene.Int())
    users = DjangoListField(gql_types.UsuarioType)
    user = graphene.Field(gql_types.UsuarioType, id=graphene.Int())
    comentarios = DjangoListField(gql_types.ComentariosType)
    temas = DjangoListField(gql_types.TemaType)
    funcoes = DjangoListField(gql_types.FuncoesType)
    texto_biblico = graphene.List(gql_types.VersiculoType, referencia=graphene.String(required=True), versao=graphene.String())

    def resolve_pergunta(root, info, tema_id):
        return random.sample(tuple(Pergunta.objects.filter(tema=Tema.objects.get(id=tema_id))), 1)

    def resolve_user(root, info, id=None):
        if info.context.user.id != id:
            if usuario_superusuario_ou_admin(info.context.user) is False and info.context.user.id != id:
                raise Exception(
                    'Somente o proprio usuario ou admins podem ver os dados de outros usuarios')

        if id is None:
            usuario = info.context.user
        else:
            usuario = User.objects.get(id=id)

        return usuario

    def resolve_texto_biblico(root, info, referencia, versao='ara'):
        version =  Versao.objects.get(sigla=str(versao).upper())
        todos_os_textos = serialize_texto_biblico(referencia, version)
        versiculos = []
        for texto in todos_os_textos:
            versiculos.extend(get_texto_biblico(
                text_info={'livro': texto[0], 'capitulo': texto[1], 'versiculo': texto[2]}, version=version))

        return versiculos