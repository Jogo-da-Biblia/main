import graphene
from app.perguntas.models import Pergunta, Tema, Referencia
from app.graphql import types as gql_types
from app.core.utils import usuario_superusuario_ou_admin
from django.contrib.auth.decorators import login_required
from graphql_jwt.decorators import login_required

class CadastrarPerguntaMutation(graphene.Mutation):
    class Arguments:
        tema_id = graphene.Int(required=True)
        enunciado = graphene.String(required=True)
        tipo_resposta = graphene.String(required=True)
        referencia_resposta_id = graphene.Int()
        outras_referencias = graphene.String()

    pergunta = graphene.Field(gql_types.PerguntasType)

    @login_required
    def mutate(self, info, tema_id, enunciado, tipo_resposta, referencia_resposta_id=None, outras_referencias=None):
        if not info.context.user.is_authenticated:
            raise Exception(
                'Voce precisa estar logado para cadastrar uma pergunta')

        tema = Tema.objects.get(id=tema_id)
        refencia_resposta = Referencia.objects.get(id=referencia_resposta_id)
        pergunta = Pergunta(tema=tema, enunciado=enunciado, tipo_resposta=tipo_resposta,
                            refencia_resposta=refencia_resposta, outras_referencias=outras_referencias, criado_por=info.context.user)
        pergunta.save()
        return CadastrarPerguntaMutation(pergunta=pergunta)
    

class EditarPerguntaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        tema_id = graphene.Int()
        enunciado = graphene.String()
        tipo_resposta = graphene.String()
        referencia_resposta_id = graphene.Int()
        outras_referencias = graphene.String()
        status = graphene.Boolean()

    pergunta = graphene.Field(gql_types.PerguntasType)

    def mutate(self, info, id, tema_id=None, enunciado=None, tipo_resposta=None, referencia_resposta_id=None, outras_referencias=None, status=None):
        if usuario_superusuario_ou_admin(info.context.user) is False and info.context.user.id != id:
            raise Exception(
                'Somente admins e o proprio usuario podem editar perguntas')

        new_fields = {'tema': tema_id, 'enunciado': enunciado, 'tipo_resposta': tipo_resposta, 'referencia_resposta': referencia_resposta_id, 'outras_referencias': outras_referencias, 'status': status}

        pergunta = Pergunta.objects.get(id=id)

        for key, value in new_fields.items():
            if value is not None:
                if key == 'tema':
                    value = Tema.objects.get(id=value)
                elif key == 'referencia_resposta':
                    value = Referencia.objects.get(id=value)
                setattr(pergunta, key, value)

        pergunta.save()
        return CadastrarPerguntaMutation(pergunta=pergunta)