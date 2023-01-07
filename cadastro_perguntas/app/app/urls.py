from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView

import rest_framework
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.settings import api_settings

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from app.schema import schema

    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.pages.urls'), name='pages'),
    
    path("api/v1/graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True
)
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True
)

'''
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
'''
