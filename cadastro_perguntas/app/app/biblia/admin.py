from django.contrib import admin
from app.biblia.models import Versiculo, Versao, Livro, Testamento

admin.site.register(Versiculo)
admin.site.register(Versao)
admin.site.register(Livro)
admin.site.register(Testamento)
