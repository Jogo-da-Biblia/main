def usuario_superusuario_ou_admin(usuario, raise_exception=False):
    if usuario.is_superuser is True or usuario.groups.filter(name='administradores').exists() is True:
        return True
    
    if raise_exception is True:
        raise Exception(
                "Somente administradores podem efetuar esta ação"
            )
    return False


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

# def receber_pontuacao_usuario(usuario):
#     pontuacao = 0
#     perguntas = Pergunta.objects.filter(
#         criado_por=User.objects.get(id=usuario.id))
#     for pergunta in perguntas:
#         pontuacao += 1  # Questao enviada
#         if pergunta.status is True:
#             # questao revidada e publicada
#             pontuacao += 2
#         else:
#             if pergunta.revisado_status is True:
#                 # questao revisada
#                 pontuacao += 1
#                 if pergunta.status is False:
#                     # questao revisada mas nao publicada
#                     pontuacao -= 1
#     return pontuacao
