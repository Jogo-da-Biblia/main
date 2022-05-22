from django.views.generic import TemplateView, ListView

from app.perguntas.models import Pergunta, Alternativa


class HomePageView(TemplateView):
    template_name = 'home.html'


class PerguntasPageView(ListView):
    model = Pergunta

    def get_queryset(self):
        return Pergunta.objects.filter(criado_por=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alternativas"] = Alternativa.objects.all()
        return context
