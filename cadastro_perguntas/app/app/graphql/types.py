import graphene
from graphene_django import DjangoObjectType
from app.biblia.models import Livro, Versiculo, Versao, Testamento  
from app.perguntas.models import Pergunta, Tema
from app.comentarios.models import Comentario 
from app.core.models import User
from django.contrib.auth.models import Group

class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = ("id", "enunciado", "tipo_resposta", "refencia_resposta", "status", "revisado_por", "tema")


class ComentariosType(DjangoObjectType):
    class Meta:
        model = Comentario
        fields = ("id", 'pergunta', 'email', 'phone', 'is_whatsapp', 'mensagem', "criado_em")


class TemaType(DjangoObjectType):
    class Meta:
        model = Tema
        fields = ("nome", "cor")


class LivroType(DjangoObjectType):
    class Meta:
        model = Livro
        fields = ("nome", "sigla", "posicao", "testamento")


class TestamentoType(DjangoObjectType):
    class Meta:
        model = Testamento


class VersaoType(DjangoObjectType):
    class Meta:
        model = Versao
        fields = ("nome", "sigla")


class VersiculoType(DjangoObjectType):
    class Meta:
        model = Versiculo
        fields = ("livro", "versao", "capitulo", "versiculo", "texto")


class FuncoesType(DjangoObjectType):
    class Meta:
        model = Group
        fields = ("name", )


class UsuarioType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_active", "is_superuser", "perguntas_criadas", "perguntas_revisadas", "perguntas_publicadas")

    pontuacao = graphene.Int()

    def resolve_pontuacao(self, info):
        if self is not None:
            return receber_pontuacao_usuario(self)
        return None