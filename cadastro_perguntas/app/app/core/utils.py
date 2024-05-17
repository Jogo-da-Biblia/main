# TODO test utils

def usuario_superusuario_ou_admin(usuario, raise_exception=False):
    if usuario.is_superuser is True or usuario.groups.filter(name='administradores').exists() is True:
        return True
    
    if raise_exception is True:
        raise Exception(
                "Somente administradores podem efetuar esta ação"
            )
    return False


def check_usuario_revisor(usuario):
    return usuario.groups.filter(name='revisores').exists()


def check_usuario_publicador(usuario):
    return usuario.groups.filter(name='publicadores').exists()


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
                    check_usuario_revisor(info.context.user)
                )
            )
            is False
        ):
            raise Exception(
                "Somente revisores e administradores podem efetuar esta ação"
            )
    return True


def check_if_user_is_admin_or_publicador(info):
    if (
            any(
                (
                    usuario_superusuario_ou_admin(info.context.user),
                    check_usuario_publicador(info.context.user)
                )
            )
            is False
        ):
            raise Exception(
                "Somente publicadores e administradores podem efetuar esta ação"
            )
    return True
