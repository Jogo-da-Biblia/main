import graphene
from graphene_django import DjangoObjectType

from app.perguntas.models import Pergunta

class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = ("id", "enunciado", "tipo_resposta", "refencia_resposta","status", "revisado_por")

class Query(graphene.ObjectType):
    all_perguntas = graphene.List(PerguntasType)

    def resolve_all_perguntas(root, info):
        # We can easily optimize query count in the resolve method
        return Pergunta.objects.all()


schema = graphene.Schema(query=Query)