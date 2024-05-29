import graphene
import graphql_jwt
from app.perguntas.views import CadastrarPerguntaMutation, EditarPerguntaMutation
from app.core.views import CadastrarUsuarioMutation, EditarUsuarioMutation, RecuperarSenhaMutation, AlterarPermissoesMutation
from app.comentarios.views import AdicionarComentarioMutation

"""
========== Mutations ==========
"""


class Mutation(graphene.ObjectType):
    # TODO
    # Utilizar input de usuario
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    editar_usuario = EditarUsuarioMutation.Field()
    recuperar_senha = RecuperarSenhaMutation.Field()
    alterar_permissoes = AlterarPermissoesMutation.Field()
    # TODO
    # Adicionar mutation que gera tema
    # Adicionar as alternativas na mutations de pergunta
    # O tipo da pergunta deve ser um Enum - pronto
    cadastrar_pergunta = CadastrarPerguntaMutation.Field()
    # Adicionar regra aonde o usuário só pode alterar a perguntas antes de ter sido revidasa
    # Somente admins e o proprio usuario podem editar a pergunta
    editar_pergunta = EditarPerguntaMutation.Field()
    # TODO
    # Adicionar mutation para revisar pergunta
    # Adicionar mutation para recusar pergunta
    # Adicionar mutation para publicar pergunta
    adicionar_comentario = AdicionarComentarioMutation.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout = graphql_jwt.Revoke.Field()
