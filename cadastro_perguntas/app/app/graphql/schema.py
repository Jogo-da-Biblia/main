import random
import smtplib
import re

import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField

from app.perguntas.models import Pergunta, Tema, Referencia
from app.comentarios.models import Comentario 
from app.core.models import User
from app.biblia.models import Livro, Versiculo, Versao
from app.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from graphene_django.forms.mutation import DjangoModelFormMutation
from app.core.forms import NewUserForm

TXT_BIBLICO_REGEX = r'^(\w+)\s+(\d+):(.*)$'

def usuario_superusuario_ou_admin(usuario):
    if usuario.is_superuser is False and any([usuario.groups.filter(name='administradores').exists(), usuario.groups.filter(name='revisores').exists(), usuario.groups.filter(name='publicadores').exists()]) is False:
        return False
    return True


def receber_pontuacao_usuario(usuario):
    pontuacao = 0
    perguntas = Pergunta.objects.filter(
        criado_por=User.objects.get(id=usuario.id))
    for pergunta in perguntas:
        pontuacao += 1  # Questao enviada
        if pergunta.status is True:
            # questao revidada e publicada
            pontuacao += 2
        else:
            if pergunta.revisado_status is True:
                # questao revisada 
                pontuacao += 1
                if pergunta.status is False:
                    # questao revisada mas nao publicada
                    pontuacao -= 1
    return pontuacao


def get_textos_biblicos(text_info: dict, version: Versao):
    textos = []
    livro = Livro.objects.get(sigla=text_info['livro'])
    for versi in text_info['versiculos']:
        current_versiculo = Versiculo.objects.filter(livro_id=livro, versao_id=version, versiculo=versi, capitulo=int(text_info['capitulo']))[0]
        textos.append(VersiculoType(livro=livro.nome, livro_abreviado=livro.sigla, versao=version.nome, versao_abreviada=version.sigla, capitulo=current_versiculo.capitulo, versiculo=current_versiculo.versiculo, texto=current_versiculo.texto))

    return textos

"""
========== Queries ==========
"""

class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = ("id", "enunciado", "tipo_resposta", "refencia_resposta", "status", "revisado_por", "tema")


class ComentariosType(DjangoObjectType):
    class Meta:
        model = Comentario
        fields = ("id", 'pergunta', 'email', 'phone', 'is_whatsapp', 'mensagem', "criado_em")


class TemaType(DjangoObjectType):
    class Meta:
        model = Tema
        fields = ("nome", "cor")


class VersiculoType(DjangoObjectType):

    livro = graphene.String()
    livro_abreviado = graphene.String()
    versao = graphene.String()
    versao_abreviada = graphene.String()

    class Meta:
        model = Versiculo
        fields = ("capitulo", "versiculo", "texto")


class FuncoesType(DjangoObjectType):
    class Meta:
        model = Group
        fields = ("name", )


class UsuarioType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff", "is_active", "is_superuser")

    pontuacao = graphene.Int()
    perguntas = graphene.List(PerguntasType)

    def resolve_pontuacao(self, info):
        if self is not None:
            return receber_pontuacao_usuario(self)
        return None

    def resolve_perguntas(self, info):
        if self is not None:
            return Pergunta.objects.filter(criado_por=self)
        return None



class Query(graphene.ObjectType):
    perguntas = DjangoListField(PerguntasType)
    pergunta = DjangoListField(PerguntasType, tema_id=graphene.Int())
    users = DjangoListField(UsuarioType)
    user = graphene.Field(UsuarioType, id=graphene.Int())
    comentarios = DjangoListField(ComentariosType)
    temas = DjangoListField(TemaType)
    funcoes = DjangoListField(FuncoesType)
    texto_biblico = graphene.List(VersiculoType, referencia=graphene.String(required=True), versao=graphene.String())

    def resolve_pergunta(root, info, tema_id):
        return random.sample(tuple(Pergunta.objects.filter(tema=Tema.objects.get(id=tema_id))), 1)

    def resolve_user(root, info, id=None):
        if info.context.user.id != id:
            if usuario_superusuario_ou_admin(info.context.user) is False and info.context.user.id != id:
                raise Exception(
                    'Somente o proprio usuario ou admins podem ver os dados de outros usuarios')

        if id is None:
            usuario = info.context.user
        else:
            usuario = User.objects.get(id=id)

        return usuario

    def resolve_texto_biblico(root, info, referencia, versao='ara'):
        version =  Versao.objects.get(sigla=str(versao).upper())

        todos_os_textos = []
        for ref in referencia.split(';'):
            if ref.strip() == '':
                continue
            match = re.match(TXT_BIBLICO_REGEX, ref.strip())
            versiculos_list = []
            if match:
                livro = match.group(1)
                capitulo = match.group(2)
                versiculos = match.group(3)

                for versi in versiculos.split(','):
                    if '-' in versi:
                        versi = range(
                            int(versi.split('-')[0]), int(versi.split('-')[1])+1)
                        versiculos_list.extend(versi)
                    else:
                        versiculos_list.append(versi)

                todos_os_textos.extend(get_textos_biblicos(
                    text_info={'livro': livro, 'capitulo': capitulo, 'versiculos': versiculos_list}, version=version))

            else:
                raise Exception('Texto biblico no formato invalido')

        return todos_os_textos


"""
========== Mutations ==========
"""

class CadastrarUsuarioMutation(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        is_staff = graphene.Boolean()

    usuario = graphene.Field(UsuarioType)

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

    usuario = graphene.Field(UsuarioType)

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


class CadastrarPerguntaMutation(graphene.Mutation):
    class Arguments:
        tema_id = graphene.Int(required=True)
        enunciado = graphene.String(required=True)
        tipo_resposta = graphene.String(required=True)
        referencia_resposta_id = graphene.Int()
        outras_referencias = graphene.String()

    pergunta = graphene.Field(PerguntasType)

    def mutate(self, info, tema_id, enunciado, tipo_resposta, referencia_resposta_id=None, outras_referencias=None):
        if not info.context.user.is_authenticated:
            raise Exception(
                'Voce precisa estar logado para cadastrar uma pergunta')

        tema = Tema.objects.get(id=tema_id)
        refencia_resposta = Referencia.objects.get(id=referencia_resposta_id)
        pergunta = Pergunta(tema=tema, enunciado=enunciado, tipo_resposta=tipo_resposta,
                            refencia_resposta=refencia_resposta, outras_referencias=outras_referencias, criado_por=info.context.user)
        pergunta.save()
        return CadastrarPerguntaMutation(pergunta=pergunta)


class EditarPerguntaMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        tema_id = graphene.Int()
        enunciado = graphene.String()
        tipo_resposta = graphene.String()
        referencia_resposta_id = graphene.Int()
        outras_referencias = graphene.String()
        status = graphene.Boolean()

    pergunta = graphene.Field(PerguntasType)

    def mutate(self, info, id, tema_id=None, enunciado=None, tipo_resposta=None, referencia_resposta_id=None, outras_referencias=None, status=None):
        if usuario_superusuario_ou_admin(info.context.user) is False and info.context.user.id != id:
            raise Exception(
                'Somente admins e o proprio usuario podem editar perguntas')

        new_fields = {'tema': tema_id, 'enunciado': enunciado, 'tipo_resposta': tipo_resposta, 'referencia_resposta': referencia_resposta_id, 'outras_referencias': outras_referencias, 'status': status}

        pergunta = Pergunta.objects.get(id=id)

        for key, value in new_fields.items():
            if value is not None:
                if key == 'tema':
                    value = Tema.objects.get(id=value)
                elif key == 'referencia_resposta':
                    value = Referencia.objects.get(id=value)
                setattr(pergunta, key, value)

        pergunta.save()
        return CadastrarPerguntaMutation(pergunta=pergunta)


class AdicionarComentarioMutation(graphene.Mutation):
    class Arguments:
        pergunta_id = graphene.Int(required=True)
        mensagem = graphene.String(required=True)
        email = graphene.String()
        phone = graphene.String()
        is_whatsapp = graphene.Boolean()

    comentario = graphene.Field(ComentariosType)

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


schema = graphene.Schema(query=Query, mutation=Mutation)
