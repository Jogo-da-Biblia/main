from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import HomePageView, PerguntasPageView, PerguntaUpdateView, PerguntaCreateView
from .views import get_versiculos, get_capitulos, get_texto_biblico


app_name = 'pages'

urlpatterns = [
    path('', login_required(PerguntasPageView.as_view()), name='minhas_perguntas'),
    path('pergunta/update/<int:pk>/', login_required(PerguntaUpdateView.as_view()), name='pergunta_update'),
    path('pergunta/add/', login_required(PerguntaCreateView.as_view()), name='pergunta_add'),
    path('pergunta/get_capitulos', get_capitulos, name='get_capitulos'),
    path('pergunta/get_versiculos', get_versiculos, name='get_versiculos'),
    path('pergunta/get_texto_biblico', get_texto_biblico, name='get_texto_biblico'),
]
