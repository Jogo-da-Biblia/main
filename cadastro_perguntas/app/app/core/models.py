from tabnanny import verbose

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from app.core.manager import UserManager

from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=56, unique=True, primary_key=True)
    email = models.EmailField(('email address'), unique=True)
    nome = models.CharField(max_length=256)
    whatsapp = models.CharField(max_length=11)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name = 'Usuário'
