from django.contrib.auth.models import AbstractUser
from django.db import models


class DjangoUser(AbstractUser):
    nome = models.CharField(max_length=256)
    email = models.CharField(max_length=126)
    whatsapp = models.CharField(max_length=11)
    senha = models.CharField(max_length=32)
    DJANGO_USER_ROLE = [
        ('COL', 'Colaborador'),
        ('REV', 'Revisor'),
        ('SUP', 'Supervisor'),
        ('ADM', 'Administrador')
    ]
    role = models.CharField(
        max_length=3, choices=DJANGO_USER_ROLE)
