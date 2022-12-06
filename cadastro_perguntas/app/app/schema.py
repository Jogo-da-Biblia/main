import graphene
from graphene_django import DjangoObjectType

from app.biblia.models import Livro

class LivroType(DjangoObjectType):
    class Meta:
        model = Livro
        fields = ("id", "nome", "posicao", "sigla", "testamento")


class Query(graphene.ObjectType):
    all_livros = graphene.List(LivroType)
    # category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_livros(root, info):
        # We can easily optimize query count in the resolve method
        # if info.context.user.is_authenticated():
        #     return Livro.objects.all()
        # else:
        #     return Livro.objects.none()
        return Livro.objects.all()

    # def resolve_category_by_name(root, info, name):
    #     try:
    #         return Category.objects.get(name=name)
    #     except Category.DoesNotExist:
    #         return None

schema = graphene.Schema(query=Query)