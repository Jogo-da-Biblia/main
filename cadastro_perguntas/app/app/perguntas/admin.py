from app.perguntas.models import Pergunta, Alternativa
from django.contrib import admin


class PerguntaAdmin(admin.ModelAdmin):
    fields = ('grupo', 'enunciado', 'tipo_resposta',
    ('referencia_resposta', 'outras_referencias'),
    ('alternativas', 'alternativas_corretas'),
    'criado_por')

    def change_view(self, request, object_id, extra_context=None):
        if request.user.has_perm('can_review_question'):
            self.fields.append('revisado_por')
            self.fields.append('revisado_em')
        if request.user.has_perm('can_publish_question'):
            self.fields.append('publicado_por')
            self.fields.append('publicado_em')
            # self.readonly_fields = ('revisado_por','revisado_em')
    
    def save_model(self, request, obj, form, change):
        # Se quem salvou é PUBLICADOR, então ele ganha o publicado_em e publicado_por
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Alternativa)
