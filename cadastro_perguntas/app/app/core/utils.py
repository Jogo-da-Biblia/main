import requests
from app.settings import GET_BIBLIA_VERSE_URL
from django.contrib.auth.models import Group


def usuario_superusuario_ou_admin(usuario, raise_exception=False):
    if (
        usuario.is_superuser is True
        or usuario.groups.filter(name="administradores").exists() is True
    ):
        return True

    if raise_exception is True:
        raise Exception("Somente administradores podem efetuar esta ação")
    return False


def check_usuario_revisor(usuario):
    return usuario.groups.filter(name="revisores").exists()


def check_usuario_publicador(usuario):
    return usuario.groups.filter(name="publicadores").exists()


def check_usuario_colaborador(usuario):
    return usuario.groups.filter(name="colaboradores").exists()


def check_if_user_is_admin_or_himself(info, user_id):
    if (
        any(
            (
                usuario_superusuario_ou_admin(info.context.user),
                user_id == info.context.user.id,
            )
        )
        is False
    ):
        raise Exception(
            "Somente o proprio usuario e administradores podem efetuar esta ação"
        )
    return True


def check_if_user_is_admin_or_revisor(info):
    if (
        any(
            (
                usuario_superusuario_ou_admin(info.context.user),
                check_usuario_revisor(info.context.user),
            )
        )
        is False
    ):
        raise Exception("Somente revisores e administradores podem efetuar esta ação")
    return True


def check_if_user_is_admin_or_colaborador(info):
    if (
        any(
            (
                usuario_superusuario_ou_admin(info.context.user),
                check_usuario_colaborador(info.context.user),
            )
        )
        is False
    ):
        raise Exception("Somente colaboradores e administradores podem efetuar esta ação")
    return True


def check_if_user_is_admin_or_publicador(info):
    if (
        any(
            (
                usuario_superusuario_ou_admin(info.context.user),
                check_usuario_publicador(info.context.user),
            )
        )
        is False
    ):
        raise Exception(
            "Somente publicadores e administradores podem efetuar esta ação"
        )
    return True


def add_user_to_admin(usuario):
    admin_group, _ = Group.objects.get_or_create(name="administradores")
    usuario.groups.add(admin_group)


def add_user_to_publicador(usuario):
    publicador_group, _ = Group.objects.get_or_create(name="publicadores")
    usuario.groups.add(publicador_group)


def add_user_to_revisores(usuario):
    revisor_group, _ = Group.objects.get_or_create(name="revisores")
    usuario.groups.add(revisor_group)


def add_user_to_colaborador(usuario):
    colaborador_group, _ = Group.objects.get_or_create(name="colaboradores")
    usuario.groups.add(colaborador_group)


def remove_user_from_admin(usuario):
    admin_group, _ = Group.objects.get_or_create(name="administradores")
    usuario.groups.remove(admin_group)


def remove_user_from_publicador(usuario):
    publicador_group, _ = Group.objects.get_or_create(name="publicadores")
    usuario.groups.remove(publicador_group)


def remove_user_from_revisores(usuario):
    revisor_group, _ = Group.objects.get_or_create(name="revisores")
    usuario.groups.remove(revisor_group)


def remove_user_from_colaborador(usuario):
    colaborador_group, _ = Group.objects.get_or_create(name="colaboradores")
    usuario.groups.remove(colaborador_group)


def get_referencia_biblica_from_web(referencia):
    params = {"q": referencia}
    response = requests.get(GET_BIBLIA_VERSE_URL, params=params)
    if response.status_code != 200:
        raise Exception("Não foi possível encontrar a referência biblica.")

    return response.json()
