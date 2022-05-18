from datetime import datetime

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test

from app.perguntas.models import Pergunta, Alternativa, Referencia


'''
Permissões:
COLABORADOR: Add, View Perguntas template externo
REVISOR: View, Change Pergunas admin
PUBLICADOR View, Change, Publish Perguntas admin
SUPERUSER ADMINISTRADOR View, Change, Publish Perguntas admin
'''


class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 0


class PerguntaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tema',
        'tipo_resposta',
        'criado_em',
        'publicado_em',
        'status',
        'revisado_status'
    )
    list_filter = ('tema', 'tipo_resposta', 'status')
    search_fields = ('tema', 'descricao')
    fields = [
        'tema', 'enunciado', 'tipo_resposta', 'refencia_resposta',
        'outras_referencias', 'criado_por',
        ('revisado_status', 'status'),
        ('revisado_por', 'revisado_em'), ('publicado_por', 'publicado_em')
    ]
    readonly_fields = (
        'revisado_por', 'revisado_em', 'publicado_por', 'publicado_em'
    )

    inlines = [AlternativaInline]

    def add_view(self, request, form_url='', extra_context=None):
        try:
            return super(PerguntaAdmin, self).add_view(
                request, form_url, extra_context
            )
        except ValidationError as e:
            print(e)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "criado_por":
            kwargs["initial"] = request.user.id
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def change_view(self, request, object_id, extra_context=None):
        if request.user.groups.filter(name='revisores').exists():
            self.fields[6] = ('revisado_status',)
        if request.user.groups.filter(name='publicadores').exists():
            self.fields[6] = ('status',)
        if request.user.groups.filter(name='administradores').exists():
            self.fields[6] = ('revisado_status', 'status')

        return super().change_view(request, object_id, extra_context)

    def save_model(self, request, obj, form, change):
        if not obj.revisado_status:
            obj.status = False

        if obj.revisado_status:
            if obj.revisado_por is None:
                obj.revisado_por = request.user
                obj.revisado_em = datetime.now()
        else:
            obj.revisado_por = None
            obj.revisado_em = None

        if obj.status:
            if obj.publicado_por is None:
                obj.publicado_por = request.user
                obj.publicado_em = datetime.now()
        else:
            obj.publicado_por = None
            obj.publicado_em = None

        super(PerguntaAdmin, self).save_model(request, obj, form, change)


class AlternativaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Alternativa, AlternativaAdmin)
admin.site.register(Referencia)
