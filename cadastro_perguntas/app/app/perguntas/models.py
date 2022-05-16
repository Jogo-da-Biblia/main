from app.biblia.models import Livro, Versiculo
from app.core.models import User
from django.db import models


class Tema(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(max_length=6)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'tema'


class Referencia(models.Model):
    id = models.AutoField(primary_key=True)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    versiculo = models.ForeignKey(
        Versiculo,
        on_delete=models.CASCADE,
        verbose_name='Versículo'
    )

    def __str__(self):
        return f"{self.livro} {self.versiculo}"

    class Meta:
        db_table = 'referencia'
        verbose_name = 'Referência'
        verbose_name_plural = 'Referências'


class Pergunta(models.Model):

    TIPO_RESPOSTA = [
        ('MES', 'Múltipla Escolha'),
        ('RCO', 'Referência Completa'),
        ('RLC', 'Referência Livro-Capítulo'),
        ('RES', 'Resposta Simples')
    ]

    id = models.AutoField(primary_key=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
    enunciado = models.TextField()

    tipo_resposta = models.CharField(
        max_length=3,
        choices=TIPO_RESPOSTA,
        verbose_name='Tipo de Resposta'
    )

    refencia_resposta = models.ForeignKey(
        Referencia,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    outras_referencias = models.ForeignKey(
        Referencia,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='outras_referencias'
    )

    status = models.BooleanField(default=True, verbose_name='Publicado')

    criado_por = models.ForeignKey(
        User,
        related_name='criado_por',
        on_delete=models.CASCADE
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    revisado_por = models.ForeignKey(
        User,
        related_name='revisado_por',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    revisado_em = models.DateTimeField(auto_now_add=True)

    publicado_por = models.ForeignKey(
        User,
        related_name='publicado_por',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    publicado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.enunciado

    class Meta:
        db_table = 'pergunta'
        verbose_name = 'Pergunta'


class Alternativa(models.Model):
    id = models.AutoField(primary_key=True)
    texto = models.TextField()
    
    alternativas = models.ForeignKey(
        Pergunta,
        related_name='alternativas',
        on_delete=models.CASCADE
    )

    alternativas_corretas = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

    class Meta:
        db_table = 'alternativa'
