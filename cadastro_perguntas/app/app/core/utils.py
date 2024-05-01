def usuario_superusuario_ou_admin(usuario):
    if usuario.is_superuser is False and any([usuario.groups.filter(name='administradores').exists(), usuario.groups.filter(name='revisores').exists(), usuario.groups.filter(name='publicadores').exists()]) is False:
        return False
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
