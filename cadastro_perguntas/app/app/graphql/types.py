import graphene
from graphene_django import DjangoObjectType
from app.perguntas.models import Pergunta, Tema
from app.comentarios.models import Comentario
from app.core.models import User


class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = (
            "id",
            "enunciado",
            "tipo_resposta",
            "referencia",
            "status",
            "revisado_por",
            "tema",
        )


class ComentariosType(DjangoObjectType):
    class Meta:
        model = Comentario
        fields = (
            "id",
            "pergunta",
            "email",
            "phone",
            "is_whatsapp",
            "mensagem",
            "criado_em",
        )


class TemaType(DjangoObjectType):
    class Meta:
        model = Tema
        fields = ("nome", "cor")


class UsuarioType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "perguntas_enviadas",
            "perguntas_revisadas",
            "perguntas_publicadas",
            "perguntas_recusadas",
        )

    pontuacao = graphene.Int()
    is_admin = graphene.Boolean()
    is_revisor = graphene.Boolean()
    is_publicador = graphene.Boolean()

    def resolve_pontuacao(self, info):
        return self.pontuacao
    
    def resolve_is_admin(self, info):
        return self.is_admin

    def resolve_is_revisor(self, info):
        return self.is_revisor

    def resolve_is_publicador(self, info):
        return self.is_publicador
