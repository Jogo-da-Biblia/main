from app.perguntas.models import Pergunta
from django.contrib import admin


class PerguntaAdmin(admin.ModelAdmin):
    fields = ['grupo', 'enunciado', 'tipo_resposta',
    'referencia_resposta', 'outras_referencias',
    'alternativas', 'alternativas_corretas',
    'criado_por']

     #def change_view(self, request, object_id, extra_context=None):
      #   if request.user.role in 'REV':
       #      self.fields.append('revisado_por')

admin.site.register(Pergunta, PerguntaAdmin)
