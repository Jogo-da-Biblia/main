import graphene
from app.perguntas.models import Pergunta, Tema
from app.graphql import types as gql_types, inputs as gql_inputs
from app.core.utils import usuario_superusuario_ou_admin
from django.contrib.auth.decorators import login_required
from graphql_jwt.decorators import login_required

# FIXME As perguntas estavam sendo criadas sem alternativas e sem referência


class CadastrarPerguntaMutation(graphene.Mutation):
    """ Cadastra uma pergunta, para executar essa ação você deve estar logado"""
    class Arguments:
        data = gql_inputs.PerguntaInput(
            required=True, description="Dados de perguntas e alternativas")  # TODO: Implementar InputType

    pergunta = graphene.Field(gql_types.PerguntasType)

    @login_required
    def mutate(self, info, tema_id, enunciado, tipo_resposta, referencia, referencia_biblica=True):
        # FIXME: Esse trecho de código se repete muitas vezes e deve ser substituído por um decorator @login_required ou função que queira criar
        if not info.context.user.is_authenticated:
            raise Exception(
                'Voce precisa estar logado para cadastrar uma pergunta')
        # TODO Em caso de referência bíblica, deve fazer uma verificação se está correto o formato da referência
        tema = Tema.objects.get(id=tema_id)
        pergunta = Pergunta(tema=tema, enunciado=enunciado, tipo_resposta=tipo_resposta,
                            referencia=referencia, referencia_biblica=referencia_biblica, criado_por=info.context.user)
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

        new_fields = {'tema': tema_id, 'enunciado': enunciado, 'tipo_resposta': tipo_resposta,
                      'referencia_resposta': referencia_resposta_id, 'outras_referencias': outras_referencias, 'status': status}

        pergunta = Pergunta.objects.get(id=id)

        for key, value in new_fields.items():
            if value is not None:
                if key == 'tema':
                    value = Tema.objects.get(id=value)
                setattr(pergunta, key, value)

        pergunta.save()
        return CadastrarPerguntaMutation(pergunta=pergunta)
