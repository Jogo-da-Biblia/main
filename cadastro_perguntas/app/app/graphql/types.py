import graphene
from graphene_django import DjangoObjectType
from app.perguntas.models import Pergunta, Tema, Alternativa
from app.comentarios.models import Comentario
from app.core.models import User
from graphene_django import DjangoListField


class AlternativaType(DjangoObjectType):
    class Meta:
        model = Alternativa
        fields = ("id", "texto", "pergunta", "correta")


class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = (
            "id",
            "tema",
            "enunciado",
            "tipo_resposta",
            "referencia",
            "referencia_biblica",
            "status",
            "criado_por",
            "criado_em",
            "aprovado_status",
            "aprovado_em",
            "aprovado_por",
            "recusado_status",
            "recusado_em",
            "recusado_por",
            "publicado_por",
            "publicado_em",
            "atualizado_em",
            "alternativas",
            "comentarios",
        )

    alternativas_corretas = DjangoListField(AlternativaType)

    def resolve_alternativas_corretas(self, info):
        return self.alternativas_corretas


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
        fields = ("id", "nome", "cor")


class UsuarioType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "perguntas_enviadas",
            "perguntas_aprovadas",
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
