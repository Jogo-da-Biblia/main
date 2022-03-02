from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import DjangoUser

admin.site.register(DjangoUser, UserAdmin)


