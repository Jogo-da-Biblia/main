import graphene
from graphene_django import DjangoObjectType
from app.core.models import User
from graphene_django.forms.mutation import DjangoFormMutation
from app.core.forms import NewUserForm



class CadastrarOuEditarUsuario(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)



class Mutations(graphene.ObjectType):
    cadastrar_ou_editar_usuario = CadastrarOuEditarUsuario.Field()
    #recuperar_senha = UpdatePergunta.Field()
    #cadastrar_ou_editar_pergunta = DeletePergunta.Field()


class MyForm(NewUserForm):
    name = forms.CharField()

class MyMutation(DjangoFormMutation):
    class Meta:
        form_class = MyForm