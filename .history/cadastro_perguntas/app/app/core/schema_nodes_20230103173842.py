import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomNode(graphene.Node):
    """
        For fetching object id instead of Node id
    """
    class Meta:
        name = 'NodeUserid'
        
    @staticmethod
    def to_global_id(type, id):
        return id
     
class UserNode(DjangoObjectType):
    # id = graphene.ID(source='pk', required=True)
    
    class Meta:
        model = User
        filter_fields = {
            'username': ['exact', 'icontains', 'istartswith'],
            'email': ['exact', 'icontains', 'istartswith'],
        }
        interfaces = (CustomNode, )