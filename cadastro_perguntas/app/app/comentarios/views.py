import graphene
from app.graphql import types as gql_types
from app.comentarios.models import Comentario
from app.perguntas.models import Pergunta


class AdicionarComentarioMutation(graphene.Mutation):
    class Arguments:
        pergunta_id = graphene.Int(required=True)
        mensagem = graphene.String(required=True)
        email = graphene.String()
        phone = graphene.String()
        is_whatsapp = graphene.Boolean()

    comentario = graphene.Field(gql_types.ComentariosType)

    def mutate(
        self, info, pergunta_id, mensagem, email=None, phone=None, is_whatsapp=True
    ):
        if info.context.user.is_authenticated:
            email = info.context.user.email
        elif str(email).strip() == "" or email is None:
            raise Exception(
                "Voce precisa estar logado ou informar um email valido para cadastrar um comentario"
            )

        mensagem = mensagem.strip()
        if mensagem == "":
            raise Exception("A mensagem nao pode ser vazia")

        pergunta = Pergunta.objects.get(id=pergunta_id)

        comentario = Comentario.objects.create(
            pergunta=pergunta,
            mensagem=mensagem,
            email=email,
            phone=phone,
            is_whatsapp=is_whatsapp,
        )

        return AdicionarComentarioMutation(comentario=comentario)
