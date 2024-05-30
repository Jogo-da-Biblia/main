import graphene
from app.perguntas.models import Pergunta, Tema
from app.graphql import types as gql_types, inputs as gql_inputs
from app.core.utils import (
    usuario_superusuario_ou_admin,
)
from app.perguntas.utils import (
    criar_nova_pergunta_via_mutation,
    check_if_referencia_biblica_is_valid,
)
from graphql_jwt.decorators import login_required

# FIXME As perguntas estavam sendo criadas sem alternativas e sem referência


class CadastrarPerguntaMutation(graphene.Mutation):
    """Cadastra uma pergunta, para executar essa ação você deve estar logado"""

    class Arguments:
        nova_pergunta = gql_inputs.PerguntaInput(
            required=True, description="Dados de perguntas e alternativas"
        )

    pergunta = graphene.Field(gql_types.PerguntasType)

    @login_required
    def mutate(self, info, nova_pergunta):
        if nova_pergunta.referencia_biblica is True:
            check_if_referencia_biblica_is_valid(referencia=nova_pergunta.referencia)

        pergunta = criar_nova_pergunta_via_mutation(
            nova_pergunta=nova_pergunta, user=info.context.user
        )

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

    def mutate(
        self,
        info,
        id,
        tema_id=None,
        enunciado=None,
        tipo_resposta=None,
        referencia_resposta_id=None,
        outras_referencias=None,
        status=None,
    ):
        if (
            usuario_superusuario_ou_admin(info.context.user) is False
            and info.context.user.id != id
        ):
            raise Exception("Somente admins e o proprio usuario podem editar perguntas")

        new_fields = {
            "tema": tema_id,
            "enunciado": enunciado,
            "tipo_resposta": tipo_resposta,
            "referencia_resposta": referencia_resposta_id,
            "outras_referencias": outras_referencias,
            "status": status,
        }

        pergunta = Pergunta.objects.get(id=id)

        for key, value in new_fields.items():
            if value is not None:
                if key == "tema":
                    value = Tema.objects.get(id=value)
                setattr(pergunta, key, value)

        pergunta.save()
        return CadastrarPerguntaMutation(pergunta=pergunta)


class CadastrarTemaMutation(graphene.Mutation):
    """Cadastra um novo Tema, para executar essa ação você deve estar logado"""

    class Arguments:
        novo_tema = gql_inputs.TemaInput(required=True, description="Dados do Tema")

    tema = graphene.Field(gql_types.TemaType)

    @login_required
    def mutate(self, info, novo_tema):
        if len(novo_tema.nome) > 50:
            raise Exception("O nome do tema deve ter no maximo 50 caracteres")
        if len(novo_tema.cor) > 6:
            raise Exception("A cor do tema deve ter no maximo 6 caracteres")

        tema = Tema.objects.create(nome=novo_tema.nome, cor=novo_tema.cor)

        return CadastrarTemaMutation(tema=tema)
