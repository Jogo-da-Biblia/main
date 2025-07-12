from django.contrib import admin

from .models import Comentario


class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'pergunta', 'email', 'phone', 'is_whatsapp', 'mensagem', 'criado_em')
    search_fields = ('email', 'phone', 'mensagem')
    list_per_page = 10
    ordering = ('-criado_em',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "email":
            kwargs["initial"] = request.user.email
            kwargs["disabled"] = True
        if db_field.name == "phone":
            kwargs["initial"] = request.user.phone
            kwargs["disabled"] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Comentario, ComentarioAdmin)
