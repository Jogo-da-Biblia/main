from django.db import models
from django.urls import reverse

from app.core.models import User


class Tema(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(max_length=6)

    def __str__(self):
        return self.nome


class Pergunta(models.Model):
    TIPO_RESPOSTA = [
        ("MES", "Múltipla Escolha"),
        ("RCO", "Referência Completa"),
        ("RLC", "Referência Livro-Capítulo"),
        ("RES", "Resposta Simples"),
    ]

    id = models.AutoField(primary_key=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    enunciado = models.TextField()

    tipo_resposta = models.CharField(
        max_length=3, choices=TIPO_RESPOSTA, verbose_name="Tipo de Resposta"
    )

    referencia = models.TextField(
        null=True,
        blank=True,
    )

    referencia_biblica = models.BooleanField(default=True)

    status = models.BooleanField(default=False, verbose_name="Publicado")

    criado_por = models.ForeignKey(
        User, related_name="perguntas_enviadas", on_delete=models.CASCADE
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    aprovado_por = models.ForeignKey(
        User,
        related_name="perguntas_aprovadas",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    aprovado_status = models.BooleanField(default=False, verbose_name="Revisado")

    aprovado_em = models.DateTimeField(null=True, blank=True)

    recusado_por = models.ForeignKey(
        User,
        related_name="perguntas_recusadas",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    recusado_status = models.BooleanField(default=False, verbose_name="Recusado")

    recusado_em = models.DateTimeField(null=True, blank=True)

    publicado_por = models.ForeignKey(
        User,
        related_name="perguntas_publicadas",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    publicado_em = models.DateTimeField(null=True, blank=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<Pergunta enunciado="{self.enunciado}">'

    class Meta:
        verbose_name = "Pergunta"

    @property
    def alternativas_corretas(self):
        return self.alternativas.filter(correta=True).all()


class Alternativa(models.Model):
    id = models.AutoField(primary_key=True)
    texto = models.TextField()

    pergunta = models.ForeignKey(
        Pergunta, related_name="alternativas", on_delete=models.CASCADE
    )
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto
