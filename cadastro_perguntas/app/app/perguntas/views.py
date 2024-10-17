import graphene
from app.perguntas.models import Pergunta, Tema
from app.graphql import types as gql_types, inputs as gql_inputs
from app.core.utils import (
    usuario_superusuario_ou_admin,
    check_if_user_is_admin_or_revisor,
    check_if_user_is_admin_or_publicador,
    check_if_user_is_admin_or_colaborador,
)
from app.perguntas.utils import (
    criar_nova_pergunta_via_mutation,
    check_if_referencia_biblica_is_valid,
    update_pergunta_values,
    aprove_pergunta,
    refuse_pergunta,
    publish_pergunta,
)
from graphql_jwt.decorators import login_required


class CadastrarPerguntaMutation(graphene.Mutation):
    """
    Mutation para cadastrar uma pergunta.
    Requer autenticação do usuário.
    """

    class Arguments:
        nova_pergunta = gql_inputs.PerguntaInput(
            required=True, description="Dados da nova pergunta e suas alternativas."
        )

    pergunta = graphene.Field(
        gql_types.PerguntasType, description="A pergunta cadastrada."
    )

    @login_required
    def mutate(self, info, nova_pergunta):
        assert check_if_user_is_admin_or_colaborador(info)

        if nova_pergunta.referencia_biblica is True:
            check_if_referencia_biblica_is_valid(referencia=nova_pergunta.referencia)

        pergunta = criar_nova_pergunta_via_mutation(
            nova_pergunta=nova_pergunta, user=info.context.user
        )

        return CadastrarPerguntaMutation(pergunta=pergunta)


class EditarPerguntaMutation(graphene.Mutation):
    """
    Mutation para editar uma pergunta.
    Requer autenticação do usuário.
    """

    class Arguments:
        pergunta_id = graphene.Int(
            required=True, description="ID da pergunta a ser editada."
        )
        novo_tema_id = graphene.Int(description="ID do novo tema da pergunta.")
        novo_enunciado = graphene.String(description="Novo enunciado da pergunta.")
        novo_tipo_resposta = gql_inputs.TipoRespostaEnum(
            description="Novo tipo de resposta da pergunta."
        )
        novo_referencia = graphene.String(description="Nova referência da pergunta.")
        novo_referencia_biblica = graphene.Boolean(
            description="Indica se a referência da pergunta é bíblica ou não."
        )
        novo_alternativas = graphene.List(
            gql_inputs.EditarAlternativaInput,
            description="Nova lista de alternativas da pergunta.",
        )

    pergunta = graphene.Field(
        gql_types.PerguntasType, description="A pergunta editada."
    )

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
            raise Exception(
                "Somente administradores e o próprio usuário podem editar perguntas."
            )

        if pergunta.aprovado_status is True:
            raise Exception("Somente perguntas não aprovadas podem ser editadas.")

        new_fields = {
            "tema": novo_tema_id,
            "enunciado": novo_enunciado,
            "tipo_resposta": novo_tipo_resposta,
            "referencia": novo_referencia,
            "referencia_biblica": novo_referencia_biblica,
            "alternativas": novo_alternativas,
        }

        update_pergunta_values(new_fields=new_fields, pergunta=pergunta)
        return EditarPerguntaMutation(pergunta=pergunta)


class AprovarPerguntaMutation(graphene.Mutation):
    """
    Mutation para aprovar uma pergunta.
    Requer autenticação do usuário com permissões de revisor ou administrador.
    """

    class Arguments:
        pergunta_id = graphene.Int(
            required=True, description="ID da pergunta a ser aprovada."
        )

    mensagem = graphene.String(
        description="Mensagem indicando o resultado da aprovação."
    )

    @login_required
    def mutate(
        self,
        info,
        pergunta_id,
    ):
        assert check_if_user_is_admin_or_revisor(info)

        pergunta = Pergunta.objects.get(id=pergunta_id)
        if pergunta.aprovado_status is True:
            raise Exception("Esta pergunta já foi aprovada")
        elif (
            pergunta.recusado_status is True
            and usuario_superusuario_ou_admin(info.context.user) is False
        ):
            raise Exception(
                "Somente administradores podem aprovar uma pergunta recusada"
            )
        elif (
            pergunta.criado_por == info.context.user
            and usuario_superusuario_ou_admin(info.context.user) is False
        ):
            raise Exception(
                "Você não pode aprovar uma pergunta criada por você mesmo. Somente administradores pordem fazer isto"
            )

        pergunta = aprove_pergunta(user=info.context.user, pergunta=pergunta)
        return AprovarPerguntaMutation(
            mensagem=f"A pergunta {pergunta.id} for aprovada com sucesso"
        )


class RecusarPerguntaMutation(graphene.Mutation):
    """
    Mutation para recusar uma pergunta.
    Requer autenticação do usuário com permissões de revisor ou administrador.
    """

    class Arguments:
        pergunta_id = graphene.Int(
            required=True, description="ID da pergunta a ser recusada."
        )

    mensagem = graphene.String(description="Mensagem indicando o resultado da recusa.")

    @login_required
    def mutate(
        self,
        info,
        pergunta_id,
    ):
        assert check_if_user_is_admin_or_revisor(info)

        pergunta = Pergunta.objects.get(id=pergunta_id)
        if pergunta.recusado_status is True:
            raise Exception("Esta pergunta já foi recusada")
        elif (
            pergunta.aprovado_status is True
            and usuario_superusuario_ou_admin(info.context.user) is False
        ):
            raise Exception(
                "Somente administradores podem recusar uma pergunta aprovada"
            )
        elif (
            pergunta.criado_por == info.context.user
            and usuario_superusuario_ou_admin(info.context.user) is False
        ):
            raise Exception(
                "Você não pode recusar uma pergunta criada por você mesmo. Somente administradores pordem fazer isto"
            )

        pergunta = refuse_pergunta(user=info.context.user, pergunta=pergunta)
        return RecusarPerguntaMutation(
            mensagem=f"A pergunta {pergunta.id} for recusada com sucesso"
        )


class PublicarPerguntaMutation(graphene.Mutation):
    """
    Mutation para publicar uma pergunta.
    Requer autenticação do usuário com permissões de publicador ou administrador.
    """

    class Arguments:
        pergunta_id = graphene.Int(
            required=True, description="ID da pergunta a ser publicada."
        )

    mensagem = graphene.String(
        description="Mensagem indicando o resultado da publicação da pergunta."
    )

    @login_required
    def mutate(
        self,
        info,
        pergunta_id,
    ):
        assert check_if_user_is_admin_or_publicador(info)

        pergunta = Pergunta.objects.get(id=pergunta_id)

        if pergunta.recusado_status is True:
            raise Exception(
                "Você não pode publicar esta pergunta pois ela foi recusada. Ela deve ser aprovada primeiro."
            )
        elif pergunta.aprovado_status is False:
            raise Exception(
                "Você não pode publicar esta pergunta pois ela não foi aprovada."
            )
        elif (
            pergunta.criado_por == info.context.user
            and usuario_superusuario_ou_admin(info.context.user) is False
        ):
            raise Exception(
                "Você não pode publicar uma pergunta criada por você mesmo. Somente administradores pordem fazer isto"
            )

        pergunta = publish_pergunta(user=info.context.user, pergunta=pergunta)
        return PublicarPerguntaMutation(
            mensagem=f"A pergunta {pergunta.id} foi publicada com sucesso."
        )


class CadastrarTemaMutation(graphene.Mutation):
    """
    Mutation para cadastrar um novo tema.
    Requer autenticação do usuário.
    """

    class Arguments:
        novo_tema = gql_inputs.TemaInput(
            required=True, description="Dados do novo tema a ser cadastrado."
        )

    tema = graphene.Field(
        gql_types.TemaType,
        description="O tema cadastrado.",
    )

    @login_required
    def mutate(self, info, novo_tema):
        if len(novo_tema.nome) > 50:
            raise Exception("O nome do tema deve ter no máximo 50 caracteres.")
        if len(novo_tema.cor) > 6:
            raise Exception("A cor do tema deve ter no máximo 6 caracteres.")

        tema = Tema.objects.create(nome=novo_tema.nome, cor=novo_tema.cor)

        return CadastrarTemaMutation(tema=tema)


class DeletarTemaMutation(graphene.Mutation):
    """
    Mutation para deletar um tema existente.
    Requer autenticação do usuário com permissões de superusuário ou administrador.
    """

    class Arguments:
        tema_id = graphene.Int(required=True, description="ID do tema a ser deletado.")

    mensagem = graphene.String(
        description="Mensagem indicando o resultado da exclusão do tema."
    )

    @login_required
    def mutate(self, info, tema_id):
        usuario_superusuario_ou_admin(info.context.user, raise_exception=True)

        tema = Tema.objects.get(id=tema_id)
        tema.delete()

        return DeletarTemaMutation(
            mensagem=f"Tema #{tema_id} foi deletado com sucesso."
        )
