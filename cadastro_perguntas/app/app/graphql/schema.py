import random
import smtplib
import re

import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField

from app.perguntas.models import Pergunta, Tema, Referencia
from app.core.models import User
from app.biblia.models import Livro, Versiculo
from app.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from graphene_django.forms.mutation import DjangoModelFormMutation
from app.core.forms import NewUserForm

TXT_BIBLICO_REGEX = r'^(\w+)\s+(\d+):(.*)$'

def is_user_superuser_or_admin(user):
    if user.is_superuser is False and any([user.groups.filter(name='administradores').exists(), user.groups.filter(name='revisores').exists(), user.groups.filter(name='publicadores').exists()]) is False:
        return False
    return True


def get_user_score(user):
    score = 0
    perguntas = Pergunta.objects.filter(
        criado_por=User.objects.get(id=user.id))
    for pergunta in perguntas:
        score += 1  # Question sended
        if pergunta.status is True:
            # reviewed and published question
            score += 2
        else:
            if pergunta.revisado_status is True:
                # reviewed question
                score += 1
                if pergunta.status is False:
                    # reviewed question but not accepted
                    score -= 1
    return score


def get_textos_biblicos(text_info: dict):
    texts = []
    book = Livro.objects.get(nome=text_info['book'])
    for verse in text_info['verses']:
        print(verse)
        texts.append(Versiculo.objects.get(
            livro_id=book, versiculo=verse, capitulo=int(text_info['chapter'])).texto)
        print(texts)

    return texts

"""
========== Queries ==========
"""

class PerguntasType(DjangoObjectType):
    class Meta:
        model = Pergunta
        fields = ("id", "enunciado", "tipo_resposta",
                  "refencia_resposta", "status", "revisado_por", "tema")


class TemaType(DjangoObjectType):
    class Meta:
        model = Tema
        fields = ("nome", "cor")


class TextoBiblicoType(graphene.ObjectType):
    textos = graphene.List(graphene.String)


class FuncoesType(DjangoObjectType):
    class Meta:
        model = Group
        fields = ("name", )


class UserType(DjangoObjectType):

    class Meta:
        model = User
        fields = ("id", "username", "email", "is_staff",
                  "is_active", "is_superuser")

    score = graphene.Int()

    def resolve_score(self, info):
        if self is not None:
            return get_user_score(self)
        return None


class UserWithScoreType(graphene.ObjectType):
    user = graphene.List(UserType)


class UserWithQuestionsType(graphene.ObjectType):
    perguntas = graphene.List(PerguntasType)
    user = graphene.Field(UserType)


class Query(graphene.ObjectType):
    perguntas = DjangoListField(PerguntasType)
    pergunta = DjangoListField(PerguntasType, tema=graphene.String())
    users = graphene.Field(UserWithScoreType)
    user = graphene.Field(UserWithQuestionsType, id=graphene.Int())
    temas = DjangoListField(TemaType)
    funcoes = DjangoListField(FuncoesType)
    texto_biblico = graphene.Field(
        TextoBiblicoType, referencia=graphene.String(required=True))

    def resolve_pergunta(root, info, tema):
        return random.sample(tuple(Pergunta.objects.filter(tema=tema)), 1)

    def resolve_users(root, info):
        return UserWithScoreType(user=User.objects.all())

    def resolve_user(root, info, id=None):
        if info.context.user.id != id:
            if is_user_superuser_or_admin(info.context.user) is False and info.context.user.id != id:
                raise Exception(
                    'Somente o proprio usuario ou admins podem ver os dados de outros usuarios')

        if id is None:
            user = info.context.user
        else:
            user = User.objects.get(id=id)

        perguntas = Pergunta.objects.filter(
            criado_por=User.objects.get(id=user.id))
        return UserWithQuestionsType(perguntas=perguntas, user=user)

    def resolve_texto_biblico(root, info, referencia):
        # match = re.match(TXT_BIBLICO_REGEX, texto)
        match = re.match(TXT_BIBLICO_REGEX, referencia)
        print(referencia)

        versiculos_list = []
        if match:
            book = match.group(1)
            chapter = match.group(2)
            verses = match.group(3)

            for verse in verses.split(','):
                if '-' in verse:
                    verse = range(
                        int(verse.split('-')[0]), int(verse.split('-')[1])+1)
                    versiculos_list.extend(verse)
                else:
                    versiculos_list.append(verse)

            all_texts = get_textos_biblicos(
                text_info={'book': book, 'chapter': chapter, 'verses': versiculos_list})

            return TextoBiblicoType(textos=all_texts)
        else:
            raise Exception('Texto biblico no formato invalido')


"""
========== Mutations ==========
"""

class CadastrarUsuarioMutation(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        is_staff = graphene.Boolean()

    user = graphene.Field(UserType)

    def mutate(self, info, username, email, password, is_staff=False):
        if is_user_superuser_or_admin(info.context.user) is False:
            raise Exception('Somente admins podem adicionar novos usuarios')
        user = User(username=username, email=email, is_staff=is_staff)
        user.set_password(password)
        user.save()
        return CadastrarUsuarioMutation(user=user)


class EditarUsuarioMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        new_username = graphene.String()
        new_email = graphene.String()
        new_password = graphene.String()
        confirm_new_passowrd = graphene.String()
        new_is_staff = graphene.Boolean()

    user = graphene.Field(UserType)

    def mutate(self, info, id, new_username=None, new_email=None, new_password=None, confirm_new_passowrd=None, new_is_staff=None):
        if is_user_superuser_or_admin(info.context.user) is False and info.context.user.id != id:
            raise Exception(
                'Somente o proprio usuario e administradores podem editar dados de usuarios')
        user = User.objects.get(id=id)

        if new_username is not None:
            user.username = new_username
        if new_email is not None:
            user.email = new_email
        if new_password is not None:
            if new_password != confirm_new_passowrd:
                raise Exception('As senhas devem ser iguais')
            user.set_password(new_password)

        if info.context.user.is_superuser:
            if new_is_staff is not None:
                user.is_staff = new_is_staff
        user.save()
        return EditarUsuarioMutation(user=user)


class RecuperarSenhaMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        email = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, user_id, email):
        if is_user_superuser_or_admin(info.context.user) is False and info.context.user.id != user_id:
            raise Exception(
                'Somente o proprio usuario e administradores podem solicitar o envio de nova senha')

        user = User.objects.get(id=user_id)

        if email != user.email:
            raise Exception(
                'O email informado não corresponde ao email do usuario')

        new_password = User.objects.make_random_password(length=10)
        user.set_password(new_password)

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

        return RecuperarSenhaMutation(message='Senha alterada e email enviado com sucesso')


class CadastrarPerguntaMutation(graphene.Mutation):
    class Arguments:
        tema_id = graphene.Int(required=True)
        enunciado = graphene.String(required=True)
        tipo_resposta = graphene.String(required=True)
        refencia_resposta_id = graphene.Int()
        outras_referencias = graphene.String()

    pergunta = graphene.Field(PerguntasType)

    def mutate(self, info, tema_id, enunciado, tipo_resposta, refencia_resposta_id=None, outras_referencias=None):
        if not info.context.user.is_authenticated:
            raise Exception(
                'Voce precisa estar logado para cadastrar uma pergunta')

        tema = Tema.objects.get(id=tema_id)
        refencia_resposta = Referencia.objects.get(id=refencia_resposta_id)
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
        refencia_resposta_id = graphene.Int()
        outras_referencias = graphene.String()

    pergunta = graphene.Field(PerguntasType)

    def mutate(self, info, id, tema_id=None, enunciado=None, tipo_resposta=None, refencia_resposta_id=None, outras_referencias=None):
        if is_user_superuser_or_admin(info.context.user) is False and info.context.user.id != id:
            raise Exception(
                'Somente admins e o proprio usuario podem editar perguntas')

        new_fields = {'tema': tema_id, 'enunciado': enunciado, 'tipo_resposta': tipo_resposta,
                      'refencia_resposta': refencia_resposta_id, 'outras_referencias': outras_referencias}

        pergunta = Pergunta.objects.get(id=id)

        for key, value in new_fields.items():
            if value is not None:
                if key == 'tema':
                    value = Tema.objects.get(id=value)
                elif key == 'refencia_resposta':
                    value = Referencia.objects.get(id=value)
                setattr(pergunta, key, value)

        pergunta.save()
        return CadastrarPerguntaMutation(pergunta=pergunta)


class Mutation(graphene.ObjectType):
    cadastrar_usuario = CadastrarUsuarioMutation.Field()
    editar_usuario = EditarUsuarioMutation.Field()
    recuperar_senha = RecuperarSenhaMutation.Field()
    cadastrarPergunta = CadastrarPerguntaMutation.Field()
    editarPergunta = EditarPerguntaMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
