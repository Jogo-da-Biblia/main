import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model


User = get_user_model()


class UserType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)
    class Meta:
        model = get_user_model()
        
        
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
        

# class CustomNode(graphene.Node):
#     """
#         For fetching object id instead of Node id
#     """
#     class Meta:
#         name = 'NodeUserid'
        
#     @staticmethod
#     def to_global_id(type, id):
#         return id
    
     
# class UserNode(DjangoObjectType):
#     # id = graphene.ID(source='pk', required=True)
    
#     class Meta:
#         model = User
#         filter_fields = {
#             'username': ['exact', 'icontains', 'istartswith'],
#             'email': ['exact', 'icontains', 'istartswith'],
#         }
#         interfaces = (CustomNode, )