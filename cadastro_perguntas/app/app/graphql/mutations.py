import graphene
import graphql_jwt
from app.perguntas.views import CadastrarPerguntaMutation, EditarPerguntaMutation
from app.core.views import CadastrarUsuarioMutation, EditarUsuarioMutation, RecuperarSenhaMutation 
from app.comentarios.views import AdicionarComentarioMutation

"""
========== Mutations ==========
"""


class Mutation(graphene.ObjectType):
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    editar_usuario = EditarUsuarioMutation.Field()
    recuperar_senha = RecuperarSenhaMutation.Field()
    # TODO revisor e publicador
    # AlterarPermissoes (Apenas admin)
        # Adicionar Revisor
        # Remover revisor
        # Adicionar Publicador
        # Remover Publicador
        # Adicionar Admin
        # Remover Admin
    # TODO tests
    cadastrar_pergunta = CadastrarPerguntaMutation.Field()
    editar_pergunta = EditarPerguntaMutation.Field()
    adicionar_comentario = AdicionarComentarioMutation.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout = graphql_jwt.Revoke.Field()
