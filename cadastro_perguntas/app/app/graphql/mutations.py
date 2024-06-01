import graphene
import graphql_jwt
from app.perguntas.views import (
    CadastrarPerguntaMutation,
    EditarPerguntaMutation,
    CadastrarTemaMutation,
    DeletarTemaMutation,
    AprovarPerguntaMutation,
    RecusarPerguntaMutation,
    PublicarPerguntaMutation
)
from app.core.views import (
    CadastrarUsuarioMutation,
    EditarUsuarioMutation,
    RecuperarSenhaMutation,
    AlterarPermissoesMutation,
)
from app.comentarios.views import AdicionarComentarioMutation, DeletarComentarioMutation

"""
========== Mutations ==========
"""


class Mutation(graphene.ObjectType):
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    editar_usuario = EditarUsuarioMutation.Field()
    recuperar_senha = RecuperarSenhaMutation.Field()
    alterar_permissoes = AlterarPermissoesMutation.Field()
    cadastrar_tema = CadastrarTemaMutation.Field()
    deletar_tema = DeletarTemaMutation.Field()
    cadastrar_pergunta = CadastrarPerguntaMutation.Field()
    editar_pergunta = EditarPerguntaMutation.Field()
    aprovar_pergunta = AprovarPerguntaMutation.Field()
    recusar_pergunta = RecusarPerguntaMutation.Field()
    publicar_pergunta = PublicarPerguntaMutation.Field()
    adicionar_comentario = AdicionarComentarioMutation.Field()
    deletar_comentario = DeletarComentarioMutation.Field()
    # TODO
    # Adicionar mutation para remover comentário
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout = graphql_jwt.Revoke.Field()
