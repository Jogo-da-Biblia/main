from click import version_option
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    DJANGO_USER_ROLE = [
        ('COLABORADOR', 'Colaborador'),
        ('REVISOR', 'Revisor'),
        ('SUPERVISOR', 'Supervisor'),
        ('ADMINISTRADOR', 'Administrador'),
    ]

    id = models.AutoField(primary_key=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    role = models.CharField(choices=DJANGO_USER_ROLE, default='COLABORADOR', max_length=20)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
