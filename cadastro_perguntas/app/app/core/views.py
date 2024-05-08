from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from app.core import utils
from app.core.models import User
from app.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from app.graphql import types as gql_types
from graphql_jwt.decorators import login_required

import smtplib
import graphene


class CadastrarUsuarioMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        name = graphene.String(required=True)
        phone = graphene.String(required=True)
        is_whatsapp = graphene.Boolean(required=False)

    usuario = graphene.Field(gql_types.UsuarioType)

    def mutate(self, info, username, email, password, name, phone, is_whatsapp=True):
        if len(password) < 6:
            raise Exception("A senha deve conter no minimo 6 caracteres")
        
        usuario = User(
            username=username,
            email=email,
            name=name,
            phone=phone,
            is_whatsapp=is_whatsapp,
        )

        usuario.set_password(password)
        usuario.save()
        return CadastrarUsuarioMutation(usuario=usuario)


class EditarUsuarioMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=False)
        name = graphene.String(required=False)
        phone = graphene.String(required=False)
        is_whatsapp = graphene.Boolean(required=False)

    usuario = graphene.Field(gql_types.UsuarioType)

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
        assert utils.check_if_user_is_admin_or_has_permission(info=info, user_id=user_id)

        usuario = User.objects.get(id=user_id)

        if password is not None:
            if len(password) < 6:
                raise Exception("A senha deve conter no minimo 6 caracteres")
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
    class Arguments:
        user_id = graphene.Int(required=True)
        email = graphene.String(required=True)

    mensagem = graphene.String()

    def mutate(self, info, user_id, email):
        assert utils.check_if_user_is_admin_or_has_permission(info=info, user_id=user_id)

        user = User.objects.get(id=user_id)

        if email != user.email:
            raise Exception("O email informado nao corresponde ao email cadastrado")

        new_password = User.objects.make_random_password(length=10)
        user.set_password(new_password)
        user.save()

        try:
            send_mail(
                subject="Recuperacao de Senha - Jogo da Biblia",
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
