import graphene
from app.perguntas.models import Pergunta, Tema
from app.graphql import types as gql_types, inputs as gql_inputs
from app.core.utils import (
    usuario_superusuario_ou_admin,
    check_if_user_is_admin_or_revisor,
    check_if_user_is_admin_or_publicador
)
from app.perguntas.utils import (
    criar_nova_pergunta_via_mutation,
    check_if_referencia_biblica_is_valid,
    update_pergunta_values,
    aprove_pergunta
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
        pergunta_id = graphene.Int(required=True)
        novo_tema_id = graphene.Int()
        novo_enunciado = graphene.String()
        novo_tipo_resposta = gql_inputs.TipoRespostaEnum()
        novo_referencia = graphene.String()
        novo_referencia_biblica = graphene.Boolean()
        novo_alternativas = graphene.List(gql_inputs.EditarAlternativaInput)

    pergunta = graphene.Field(gql_types.PerguntasType)

    @login_required
    def mutate(
        self,
        info,
        pergunta_id,
        novo_tema_id=None,
        novo_enunciado=None,
        novo_tipo_resposta=None,
        novo_referencia=None,
        novo_referencia_biblica=None,
        novo_alternativas=None,
    ):
        pergunta = Pergunta.objects.get(id=pergunta_id)
        if (
            usuario_superusuario_ou_admin(info.context.user) is False
            and info.context.user.id != pergunta.criado_por.id
        ):
            raise Exception("Somente admins e o proprio usuario podem editar perguntas")

        if pergunta.revisado_status is True:
            raise Exception("Somente perguntas não revisadas podem ser editadas")

        new_fields = {
            "tema": novo_tema_id,
            "enunciado": novo_enunciado,
            "tipo_resposta": novo_tipo_resposta,
            "referencia": novo_referencia,
            "referencia_biblica": novo_referencia_biblica,
            "alternativas": novo_alternativas,
        }

        update_pergunta_values(new_fields=new_fields, pergunta=pergunta)
        return CadastrarPerguntaMutation(pergunta=pergunta)


class AprovarPerguntaMutation(graphene.Mutation):
    class Arguments:
        pergunta_id = graphene.Int(required=True)

    mensagem = graphene.String()

    @login_required
    def mutate(
        self,
        info,
        pergunta_id,
    ):
        assert check_if_user_is_admin_or_revisor(info)

        pergunta = Pergunta.objects.get(id=pergunta_id)
        if pergunta.revisado_status is True:
            raise Exception("Esta pergunta já foi revisada")

        pergunta = aprove_pergunta(user=info.context.user, pergunta=pergunta)
        return AprovarPerguntaMutation(mensagem=f"A pergunta {pergunta.id} for aprovada com sucesso")


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


class DeletarTemaMutation(graphene.Mutation):
    class Arguments:
        tema_id = graphene.Int()

    mensagem = graphene.String()

    @login_required
    def mutate(self, info, tema_id):
        usuario_superusuario_ou_admin(info.context.user, raise_exception=True)

        tema = Tema.objects.get(id=tema_id)
        tema.delete()

        return DeletarTemaMutation(mensagem=f"Tema #{tema_id} deletado com sucesso")
