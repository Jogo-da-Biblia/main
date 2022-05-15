from django.contrib import admin

from .models import Comentario


class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'pergunta', 'email', 'phone', 'is_whatsapp', 'mensagem', 'criado_em')
    list_filter = ('is_whatsapp',)
    search_fields = ('email', 'phone', 'mensagem')
    list_per_page = 10
    ordering = ('-criado_em',)


admin.site.register(Comentario, ComentarioAdmin)
