from app.perguntas.models import Pergunta
from django.contrib import admin


class PerguntaAdmin(admin.ModelAdmin):
    fields = ['grupo', 'enunciado', 'tipo_resposta',
    'referencia_resposta', 'outras_referencias',
    'alternativas', 'alternativas_corretas',
    'criado_por', 'revisado_por', 'publicado_por']

admin.site.register(Pergunta, PerguntaAdmin)
