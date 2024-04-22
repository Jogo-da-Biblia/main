import graphene
import graphql_jwt
from . import types as gql_types
from app.perguntas.views import CadastrarPerguntaMutation, EditarPerguntaMutation

from app.perguntas.models import Pergunta, Tema
from app.comentarios.models import Comentario 
from app.core.models import User
from app.biblia.models import Livro, Versiculo, Versao, Testamento  
from app.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

import smtplib

"""
========== Mutations ==========
"""

class CadastrarUsuarioMutation(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        is_staff = graphene.Boolean()

    usuario = graphene.Field(gql_types.UsuarioType)

    def mutate(self, info, username, email, password, is_staff=False):
        if usuario_superusuario_ou_admin(info.context.user) is False:
            raise Exception('Somente admins podem adicionar novos usuarios')
        usuario = User(username=username, email=email, is_staff=is_staff)
        usuario.set_password(password)
        usuario.save()
        return CadastrarUsuarioMutation(usuario=usuario)


class EditarUsuarioMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        new_username = graphene.String()
        new_email = graphene.String()
        new_password = graphene.String()
        confirm_new_passowrd = graphene.String()
        new_is_staff = graphene.Boolean()

    usuario = graphene.Field(gql_types.UsuarioType)

    def mutate(self, info, id, new_username=None, new_email=None, new_password=None, confirm_new_passowrd=None, new_is_staff=None):
        if usuario_superusuario_ou_admin(info.context.user) is False and info.context.user.id != id:
            raise Exception(
                'Somente o proprio usuario e administradores podem editar dados de usuarios')
        usuario = User.objects.get(id=id)

        if new_username is not None:
            usuario.username = new_username
        if new_email is not None:
            usuario.email = new_email
        if new_password is not None:
            if new_password != confirm_new_passowrd:
                raise Exception('As senhas devem ser iguais')
            usuario.set_password(new_password)

        if info.context.user.is_superuser:
            if new_is_staff is not None:
                usuario.is_staff = new_is_staff
        usuario.save()
        return EditarUsuarioMutation(usuario=usuario)


class RecuperarSenhaMutation(graphene.Mutation):
    class Arguments:
        usuario_id = graphene.Int(required=True)
        email = graphene.String(required=True)

    mensagem = graphene.String()

    def mutate(self, info, usuario_id, email):
        if usuario_superusuario_ou_admin(info.context.user) is False and info.context.user.id != usuario_id:
            raise Exception(
                'Somente o proprio usuario e administradores podem solicitar o envio de nova senha')

        usuario = User.objects.get(id=usuario_id)

        if email != usuario.email:
            raise Exception(
                'O email informado não corresponde ao email do usuario')

        new_password = User.objects.make_random_password(length=10)
        usuario.set_password(new_password)

        try:
            send_mail(
                subject='Recuperacao de Senha - Jogo da Biblia',
                message='Recebemos seu pedido de recuperação de senha, esta é a sua nova senha de acesso: ' + new_password,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except smtplib.SMTPException:
            raise Exception(
                'Senha alterada com sucesso\nErro durante o envio do email')

        return RecuperarSenhaMutation(mensagem='Senha alterada e email enviado com sucesso')


class AdicionarComentarioMutation(graphene.Mutation):
    class Arguments:
        pergunta_id = graphene.Int(required=True)
        mensagem = graphene.String(required=True)
        email = graphene.String()
        phone = graphene.String()
        is_whatsapp = graphene.Boolean()

    comentario = graphene.Field(gql_types.ComentariosType)

    def mutate(self, info, pergunta_id, mensagem, email=None, phone=None, is_whatsapp=True):

        if info.context.user.is_authenticated:
            email = info.context.user.email
        elif str(email).strip() == '' or email is None:
            raise Exception('Voce precisa estar logado ou informar um email valido para cadastrar um comentario')
        
        mensagem = mensagem.strip()
        if mensagem == '':
            raise Exception('A mensagem nao pode ser vazia')

        pergunta = Pergunta.objects.get(id=pergunta_id)
        comentario = Comentario(pergunta=pergunta, mensagem=mensagem, email=email, phone=phone, is_whatsapp=is_whatsapp)
        comentario.save()

        return AdicionarComentarioMutation(comentario=comentario)
    

class Mutation(graphene.ObjectType):
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    editar_usuario = EditarUsuarioMutation.Field()
    recuperar_senha = RecuperarSenhaMutation.Field()
    cadastrarPergunta = CadastrarPerguntaMutation.Field()
    editarPergunta = EditarPerguntaMutation.Field()
    adicionarComentario = AdicionarComentarioMutation.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    logout = graphql_jwt.Revoke.Field()