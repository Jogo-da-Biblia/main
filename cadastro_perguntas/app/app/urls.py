"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from graphql_jwt.middleware import JSONWebTokenMiddleware
from django.views.decorators.csrf import csrf_exempt

from app.graphql.schema import schema

class DebugMiddleware:
    def resolve(self, next, root, info, **kwargs):
        print("Authorization Header:", info.context.headers.get("Authorization"))
        print("User:", info.context.user)
        return next(root, info, **kwargs)
        
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),
    path(
        "graphql",
        GraphQLView.as_view(graphiql=True, schema=schema),
        name="graphql",
    ),
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
