from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.db import models

from app.core.manager import UserManager
from app.core import utils

import re


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters"
        ),
        validators=[
            validators.RegexValidator(
                re.compile("^[\w.@+-]+$"), _("Enter a valid username."), _("invalid")
            )
        ],
    )
    email = models.EmailField(("email address"), unique=True)
    name = models.CharField(max_length=256)
    phone = models.CharField(max_length=11)
    is_whatsapp = models.BooleanField("É Whatsapp?", default=True)
    is_active = models.BooleanField("Está ativo?", default=True)
    created_at = models.DateTimeField("Data de Cadastro", auto_now_add=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        verbose_name = "Usuário"

    @property
    def pontuacao(self):
        # Perguntas enviadas somarão um ponto
        # Caso a pergunta seja recusada a pessoa continua com apenas um ponto
        # Perguntas enviadas e aprovadas somarão dois pontos
        # Perguntas enviadas, aprovadas e publicadas somarão três pontos

        perguntas_enviadas = self.perguntas_enviadas
        
        total = perguntas_enviadas.count() # Soma + 1 para todas as perguntas enviadas
        perguntas_enviadas = perguntas_enviadas.exclude(recusado_status=True) # Remove as perguntas recusadas

        total += perguntas_enviadas.filter(aprovado_status=True).count()  # Soma + 1 para todas as perguntas aprovadas
        perguntas_enviadas = perguntas_enviadas.exclude(aprovado_status=False) # Remove as perguntas nao aprovadas
        
        total += perguntas_enviadas.filter(publicado_por__isnull=False).count() # + 1 para todas as perguntas publicadas

        return total

    @property
    def is_admin(self):
        return utils.usuario_superusuario_ou_admin(usuario=self)

    @property
    def is_revisor(self):
        return utils.check_usuario_revisor(usuario=self)

    @property
    def is_publicador(self):
        return utils.check_usuario_publicador(usuario=self)
    
    @property
    def is_colaborador(self):
        return utils.check_usuario_colaborador(usuario=self)
