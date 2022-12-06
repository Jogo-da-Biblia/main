from django.contrib import admin
from app.biblia.models import Versiculo, Versao, Livro, Testamento, TotalVersiculo

admin.site.register(Versiculo)
admin.site.register(Versao)
admin.site.register(Livro)
admin.site.register(Testamento)
admin.site.register(TotalVersiculo)
