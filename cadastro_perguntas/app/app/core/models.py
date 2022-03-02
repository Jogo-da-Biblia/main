from tabnanny import verbose

from django.contrib.auth.models import AbstractUser
from django.db import models


class DjangoUser(AbstractUser):
    DJANGO_USER_ROLE = [
        ('COL', 'Colaborador'),
        ('REV', 'Revisor'),
        ('SUP', 'Supervisor'),
        ('ADM', 'Administrador')
    ]

    nome = models.CharField(max_length=256)
    email = models.CharField(max_length=126)
    whatsapp = models.CharField(max_length=11)
    senha = models.CharField(max_length=32)
    role = models.CharField(
        max_length=3, choices=DJANGO_USER_ROLE)
    
    class Meta:
        verbose_name = 'Usuário'
