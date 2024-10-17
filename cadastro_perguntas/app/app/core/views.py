<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from app.core.utils import usuario_superusuario_ou_admin
=======
from app.core import utils
>>>>>>> 0dc75f0c16c0ad414fbf6634b7a63177afddf74c
from app.core.models import User
from app.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from app.graphql import types as gql_types
from app.graphql import inputs as gql_inputs
from graphql_jwt.decorators import login_required

import smtplib
import graphene


class CadastrarUsuarioMutation(graphene.Mutation):
    """
    Mutation para cadastrar um novo usuário.
    """

    class Arguments:
        novo_usuario = gql_inputs.UsuarioInput(
            required=True, description="Dados do novo usuário a ser cadastrado."
        )

    usuario = graphene.Field(gql_types.UsuarioType, description="O usuário cadastrado.")

<<<<<<< HEAD
    def mutate(self, info, username, email, password, is_staff=False):
        usuario = User(username=username, email=email, is_staff=is_staff)
        usuario.set_password(password)
=======
    def mutate(self, info, novo_usuario):
        if len(novo_usuario.password) < 6:
            raise Exception("A senha deve conter no mínimo 6 caracteres.")

        usuario = User(
            username=novo_usuario.username,
            email=novo_usuario.email,
            name=novo_usuario.name,
            phone=novo_usuario.phone,
            is_whatsapp=novo_usuario.is_whatsapp,
        )

        usuario.set_password(novo_usuario.password)
>>>>>>> 0dc75f0c16c0ad414fbf6634b7a63177afddf74c
        usuario.save()

        utils.add_user_to_colaborador(usuario=usuario)
        
        return CadastrarUsuarioMutation(usuario=usuario)


class EditarUsuarioMutation(graphene.Mutation):
    """
    Mutation para editar informações de um usuário existente.
    """

    class Arguments:
        user_id = graphene.Int(
            required=True, description="ID do usuário a ser editado."
        )
        username = graphene.String(description="Novo nome de usuário.")
        email = graphene.String(description="Novo endereço de email.")
        password = graphene.String(description="Nova senha.")
        name = graphene.String(description="Novo nome.")
        phone = graphene.String(description="Novo número de telefone.")
        is_whatsapp = graphene.Boolean(
            description="Indica se o novo número de telefone é do WhatsApp."
        )

    usuario = graphene.Field(gql_types.UsuarioType, description="O usuário editado.")

    @login_required
    def mutate(
        self,
        info,
        user_id,
        username=None,
        email=None,
        phone=None,
        is_whatsapp=None,
        name=None,
        password=None,
    ):
        assert utils.check_if_user_is_admin_or_himself(info=info, user_id=user_id)

        usuario = User.objects.get(id=user_id)

        if password is not None:
            if len(password) < 6:
                raise Exception("A senha deve conter no mínimo 6 caracteres.")
            usuario.set_password(password)

        updates = {
            "username": username,
            "email": email,
            "phone": phone,
            "is_whatsapp": is_whatsapp,
            "name": name,
        }

        for attr, value in updates.items():
            if value is not None:
                setattr(usuario, attr, value)

        usuario.save()
        return EditarUsuarioMutation(usuario=usuario)


class RecuperarSenhaMutation(graphene.Mutation):
    """
    Mutation para recuperar a senha de um usuário.
    """

    class Arguments:
        user_id = graphene.Int(
            required=True, description="ID do usuário que deseja recuperar a senha."
        )
        email = graphene.String(
            required=True, description="Email do usuário para enviar a nova senha."
        )

    mensagem = graphene.String(
        description="Mensagem indicando o status da operação de recuperação de senha."
    )

    def mutate(self, info, user_id, email):
        assert utils.check_if_user_is_admin_or_himself(info=info, user_id=user_id)

        user = User.objects.get(id=user_id)

        if email != user.email:
            raise Exception("O email informado não corresponde ao email cadastrado.")

        new_password = User.objects.make_random_password(length=10)
        user.set_password(new_password)
        user.save()

        try:
            send_mail(
                subject="Recuperação de Senha - Jogo da Bíblia",
                message="Recebemos seu pedido de recuperação de senha, esta é a sua nova senha de acesso: "
                + new_password,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except smtplib.SMTPException:
            return RecuperarSenhaMutation(
                mensagem="Senha alterada com sucesso\nErro durante o envio do email"
            )

        return RecuperarSenhaMutation(
            mensagem="Senha alterada e email enviado com sucesso"
        )


class RoleEnum(graphene.Enum):
    ADMIN = "admin"
    PUBLICADOR = "publicador"
    REVISOR = "revisor"
    COLABORADOR = "colaborador"


class ActionEnum(graphene.Enum):
    ADD = "Adicionar"
    REMOVE = "Remover"


class AlterarPermissoesMutation(graphene.Mutation):
    """
    Mutation para alterar as permissões de um usuário.
    """

    class Arguments:
        user_id = graphene.Int(
            required=True, description="ID do usuário para alterar as permissões."
        )
        role = RoleEnum(
            required=True, description="Permissão que será adicionada ou removida."
        )
        action = ActionEnum(
            required=True, description="Ação para adicionar ou remover permissões."
        )

    usuario = graphene.Field(
        gql_types.UsuarioType,
        description="Usuário cujas permissões foram alteradas.",
    )

    @login_required
    def mutate(
        self,
        info,
        user_id,
        role,
        action,
    ):
        assert utils.usuario_superusuario_ou_admin(
            usuario=info.context.user, raise_exception=True
        )

        usuario = User.objects.get(id=user_id)

        if role == RoleEnum.REVISOR:
            utils.add_user_to_revisores(
                usuario=usuario
            ) if action == ActionEnum.ADD else utils.remove_user_from_revisores(
                usuario=usuario
            )
        elif role == RoleEnum.PUBLICADOR:
            utils.add_user_to_publicador(
                usuario=usuario
            ) if action == ActionEnum.ADD else utils.remove_user_from_publicador(
                usuario=usuario
            )
        elif role == RoleEnum.ADMIN:
            utils.add_user_to_admin(
                usuario=usuario
            ) if action == ActionEnum.ADD else utils.remove_user_from_admin(
                usuario=usuario
            )
        elif role == RoleEnum.COLABORADOR:
            utils.add_user_to_colaborador(
                usuario=usuario
            ) if action == ActionEnum.ADD else utils.remove_user_from_colaborador(
                usuario=usuario
            )

        usuario.save()
        return AlterarPermissoesMutation(usuario=usuario)
