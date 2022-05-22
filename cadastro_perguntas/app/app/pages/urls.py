from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import HomePageView, PerguntasPageView#, PerguntaCreateView, PerguntaUpdateView


app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('perguntas', login_required(PerguntasPageView.as_view()), name='minhas_perguntas'),
]
