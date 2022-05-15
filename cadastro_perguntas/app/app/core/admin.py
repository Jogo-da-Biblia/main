from re import S
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp, EmailAddress

from .models import User


class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email',)
    list_filter = ('email', 'is_staff', 'is_active',)
    # Campos que aparecem na edição do usuário
    fieldsets = (
        (None, {'fields': ('email', 'name', 'phone', 'groups', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # Campos que aparecem na adição de um usuário
    add_fieldsets = (
        (None, {
            'fields': ('username', 'name', 'email', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Site)

admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(EmailAddress)
