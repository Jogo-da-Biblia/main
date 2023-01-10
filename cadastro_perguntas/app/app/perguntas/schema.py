import graphene as g
from graphene_django import DjangoObjectType

from .models import *


class TemaNode(DjangoObjectType):
    class Meta:
        model = Tema


class ReferenciaNode(DjangoObjectType):
    class Meta:
        model = Referencia
        filter_fields = ["livro", "versiculo"]
        fields = "__all__"
        interfaces = (g.relay.Node, )
    

class PerguntaNode(DjangoObjectType):
    class Meta:
        model = Pergunta
        filter_fields = {
            "tema": ['exact'],
            "tipo_resposta": ['exact', 'icontains', 'istartswith'],
            "status": ['exact', 'istartswith'],
        }
        interfaces = (g.relay.Node, )
        fields = "__all__"


class AlternativaNode(DjangoObjectType):
    class Meta:
        model = Alternativa
        interfaces = (g.relay.Node, )
        fields = "__all__"
