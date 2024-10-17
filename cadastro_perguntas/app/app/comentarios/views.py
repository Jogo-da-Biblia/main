import graphene
from app.graphql import types as gql_types
from app.comentarios.models import Comentario
from app.perguntas.models import Pergunta
from app.core.utils import usuario_superusuario_ou_admin
from graphql_jwt.decorators import login_required

class AdicionarComentarioMutation(graphene.Mutation):
    """
    Mutation para adicionar um comentário a uma pergunta.
    """

    class Arguments:
        pergunta_id = graphene.Int(
            required=True, description="ID da pergunta à qual o comentário será adicionado."
        )
        mensagem = graphene.String(
            required=True, description="Mensagem do comentário a ser adicionado."
        )
        email = graphene.String(
            description="E-mail do usuário que está adicionando o comentário."
        )
        phone = graphene.String(
            description="Número de telefone do usuário que está adicionando o comentário."
        )
        is_whatsapp = graphene.Boolean(
            description="Indica se o número de telefone fornecido é do WhatsApp."
        )

    comentario = graphene.Field(
        gql_types.ComentariosType,
        description="Comentário adicionado à pergunta.",
    )

    def mutate(
        self, info, pergunta_id, mensagem, email=None, phone=None, is_whatsapp=True
    ):
        if info.context.user.is_authenticated:
            email = info.context.user.email
        elif str(email).strip() == "" or email is None:
            raise Exception(
                "Você precisa estar logado ou informar um email válido para cadastrar um comentário"
            )

        mensagem = mensagem.strip()
        if mensagem == "":
            raise Exception("A mensagem não pode ser vazia")

        pergunta = Pergunta.objects.get(id=pergunta_id)

        comentario = Comentario.objects.create(
            pergunta=pergunta,
            mensagem=mensagem,
            email=email,
            phone=phone,
            is_whatsapp=is_whatsapp,
        )

        return AdicionarComentarioMutation(comentario=comentario)


class DeletarComentarioMutation(graphene.Mutation):
    """
    Mutation para deletar um comentário.
    """

    class Arguments:
        comentario_id = graphene.Int(
            description="ID do comentário a ser deletado."
        )

    mensagem = graphene.String(
        description="Mensagem indicando o sucesso da operação de exclusão do comentário."
    )

    @login_required
    def mutate(self, info, comentario_id):
        usuario_superusuario_ou_admin(info.context.user, raise_exception=True)

        comentario = Comentario.objects.get(id=comentario_id)
        comentario.delete()

        return DeletarComentarioMutation(mensagem=f"Comentário #{comentario_id} deletado com sucesso")
