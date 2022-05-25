from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.template import RequestContext

from app.perguntas.models import Pergunta, Alternativa
from app.perguntas.forms import AlternativaForm
from app.biblia.models import Versiculo


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


class PerguntaCreateView(CreateView):
    model = Pergunta
    template_name_suffix: str = '_add'
    fields = ['tema', 'enunciado', 'tipo_resposta']
    success_url = '/'

    def form_valid(self, form):
        form.instance.criado_por = self.request.user

        AlternativasFormSet = inlineformset_factory(Pergunta, Alternativa, form=AlternativaForm)
        # if self.request.method == 'POST':
        #     formset = AlternativasFormSet(self.request.POST, instance=form.instance)
        #     if formset.is_valid():
        #         formset.save(commit=False)

        formset = AlternativasFormSet(self.request.POST, instance=form.instance)
        formset.instance = self.object
        formset.save(commit=False)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alternativas"] = Alternativa.objects.all()
        context["versiculos"] = Versiculo.objects.all()

        AlternativasFormSet = inlineformset_factory(Pergunta, Alternativa, form=AlternativaForm, extra=1)
        context["formset"] = AlternativasFormSet()
        return context

    def addAlternativas(self, request):
        AlternativasFormSet = formset_factory(Alternativa, can_delete=True, extra=1)
        if self.request.method == 'POST':
            formset = AlternativasFormSet(self.request.POST)
            if formset.is_valid():
                saved = formset.save(commit=False)
                saved.save()
                # messages.success(request, "Submitted! Thank you.")
        else:
            formset = AlternativasFormSet()
        return render(
            'pergunta_add.html',
            request
        )


class PerguntaUpdateView(UpdateView):
    model = Pergunta
    fields = '__all__'
    success_url = '/'
