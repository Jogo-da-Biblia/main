from django.forms import BaseInlineFormSet, inlineformset_factory, formset_factory
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, UpdateView, CreateView

from app.perguntas.models import Pergunta, Alternativa
from app.perguntas.forms import AlternativaForm, ReferenciaForm
from app.biblia.models import Versiculo, Livro, Versao
from app.biblia.forms import VersiculoForm


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


class PerguntaCreateView(CreateView, BaseInlineFormSet):
    model = Pergunta
    template_name = 'perguntas/pergunta_add.html'
    fields = ['tema', 'enunciado', 'tipo_resposta', 'outras_referencias']
    success_url = '/'

    def form_valid(self, form):
        form.instance.criado_por = self.request.user

        AlternativasFormSet = inlineformset_factory(Pergunta, Alternativa, form=AlternativaForm)
        if self.request.method == 'POST':
            formset = AlternativasFormSet(self.request.POST, instance=form.instance)
            if formset.is_valid() and form.is_valid():
                form.save()
                formset.save()

            referencia_form = ReferenciaForm(self.request.POST)
            if referencia_form.is_valid():
                referencia_form.save()
                form.instance.refencia_resposta = referencia_form.instance
                form.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["livros"] = Livro.objects.all()
        context['versoes'] = Versao.objects.all()

        AlternativasFormSet = inlineformset_factory(Pergunta, Alternativa, form=AlternativaForm, extra=1, can_delete=True)
        context["formset"] = AlternativasFormSet()
        return context


class PerguntaUpdateView(UpdateView):
    model = Pergunta
    fields = ['tema', 'enunciado', 'tipo_resposta', 'refencia_resposta', 'outras_referencias']
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        AlternativasFormSet = inlineformset_factory(Pergunta, Alternativa, form=AlternativaForm, extra=0, can_delete=True)
        context["formset"] = AlternativasFormSet(instance=self.object)

        context["referencia_form"] = ReferenciaForm(instance=self.object.refencia_resposta)
        context["versiculo_form"] = VersiculoForm(instance=self.object.refencia_resposta.versiculo)

        return context

    def form_valid(self, form):
        AlternativasFormSet = inlineformset_factory(Pergunta, Alternativa, form=AlternativaForm)
        if self.request.method == 'POST':
            formset = AlternativasFormSet(self.request.POST, instance=form.instance)
            if formset.is_valid():
                formset.save()

        return super().form_valid(form)


def get_capitulos(request):
    if request.method == 'POST':
        versao = Versiculo.objects.filter(versao_id=request.POST['versao'])
        capitulos = versao.filter(livro_id=request.POST['livro']).distinct('capitulo')
        return JsonResponse(list(capitulos.values("capitulo")), safe=False)


def get_versiculos(request):
    if request.method == 'POST':
        versao = Versiculo.objects.filter(versao_id=request.POST['versao'])
        capitulos = versao.filter(livro_id=request.POST['livro'])
        versiculos = capitulos.filter(capitulo=request.POST['capitulo']).distinct('versiculo')
        return JsonResponse(list(versiculos.values('versiculo')), safe=False)


def get_texto_biblico(request):
    if request.method == 'POST':
        versao = Versiculo.objects.filter(versao_id=request.POST['versao'])
        capitulos = versao.filter(livro_id=request.POST['livro'])
        versiculos = capitulos.filter(capitulo=request.POST['capitulo'])
        texto_biblico = versiculos.filter(versiculo=request.POST['versiculo'])
        return JsonResponse(texto_biblico.last().texto, safe=False)
