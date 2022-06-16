from datetime import datetime

from django.contrib import admin
from django.core.exceptions import ValidationError

from app.perguntas.models import Pergunta, Alternativa, Referencia
from app.comentarios.models import Comentario


'''
Permissões:
COLABORADOR: Add, View Perguntas template frontend
REVISOR: View, Change, Review Perguntas admin
PUBLICADOR View, Change, Publish Perguntas admin
SUPERVISOR all permissions (Review only or Publish only) admin
ADMINISTRADOR all permissions admin
'''


class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 0


class ComentarioInline(admin.TabularInline):
    model = Comentario
    fields = ('mensagem',)
    extra = 0

    # Garannte que os campos email e phone serão automaticamente preenchidos
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "email":
            kwargs["initial"] = request.user.email
            kwargs["disabled"] = True

        if db_field.name == "phone":
            kwargs["initial"] = request.user.phone
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Garante que os campos email e phone estarão na requisição POST
    def has_add_permission(self, request, obj):
        if request.method == 'POST':
            self.fields = ('mensagem', 'email', 'phone')
        return super().has_add_permission(request, obj)


class PerguntaAdmin(admin.ModelAdmin):
    change_form_template = 'admin/perguntas/change_form.html'
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

    inlines = [AlternativaInline, ComentarioInline]

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

    # Garante que publicadores e revisores alterem apenas seus status
    def change_view(self, request, object_id, extra_context=None):
        initial_readonly_fields = ('revisado_por', 'revisado_em', 'publicado_por', 'publicado_em')
        if request.user.groups.filter(name='revisores').exists():
            self.readonly_fields += ('status',)
        elif request.user.groups.filter(name='publicadores').exists():
            obj = self.get_object(request, object_id)
            if obj.revisado_status:
                self.readonly_fields += ('revisado_status',)
            else:
                self.readonly_fields += ('status', 'revisado_status')
        elif request.user.groups.filter(name='supervisores').exists() or\
                request.user.groups.filter(name='administradores').exists() or request.user.is_superuser:
            self.readonly_fields = initial_readonly_fields
        else:
            self.readonly_fields += ('status', 'revisado_status')

        return super().change_view(request, object_id, extra_context)

    def double_check(self, request, obj):
        if request.user.groups.filter(name='administradores').exists() \
                or request.user.is_superuser:
            return True
        if obj.publicado_por == obj.revisado_por:
            obj.status = False

    def save_model(self, request, obj, form, change):
        # Perguntas não revisadas não podem ser publicadas
        if not obj.revisado_status:
            obj.status = False

        # Altera o nome do revisor se o status for alterado
        if obj.revisado_status:
            if obj.revisado_por is None:
                obj.revisado_por = request.user
                obj.revisado_em = datetime.now()
        else:
            obj.revisado_por = None
            obj.revisado_em = None

        self.double_check(request, obj)

        # Altera o nome do publicador se o status for alterado
        if obj.status:
            if obj.publicado_por is None:
                obj.publicado_por = request.user
                obj.publicado_em = datetime.now()
        else:
            obj.publicado_por = None
            obj.publicado_em = None

        super(PerguntaAdmin, self).save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if "revisar" in request.POST:
            pass
        if "publicar" in request.POST:
            pass
        return super().response_change(request, obj)


class AlternativaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Alternativa, AlternativaAdmin)
admin.site.register(Referencia)
