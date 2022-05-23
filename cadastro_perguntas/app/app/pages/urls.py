from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import HomePageView, PerguntasPageView, PerguntaUpdateView#, PerguntaCreateView, 


app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('minhas_perguntas/', login_required(PerguntasPageView.as_view()), name='minhas_perguntas'),
    path('pergunta/update/<int:pk>/', login_required(PerguntaUpdateView.as_view()), name='pergunta_update'),
]
