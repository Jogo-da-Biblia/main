from tabnanny import verbose

from app.biblia.models import Livro, Versiculo
from app.core.models import User
from django.db import models
from django.db.models import ForeignKey


class Grupo(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(max_length=6)

    class Meta:
        db_table = 'grupo'


class Referencia(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    versiculo = models.ForeignKey(Versiculo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'referencia'


class Alternativa(models.Model):
    texto = models.TextField()

    class Meta:
        db_table = 'alternativa'


class Pergunta(models.Model):

    TIPO_RESPOSTA = [
        ('MES', 'Múltipla Escolha'),
        ('RCO', 'Referência Completa'),
        ('RLC', 'Referência Livro-Capítulo'),
        ('RES', 'Resposta Simples')
    ]

    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    enunciado = models.TextField()
    tipo_resposta = models.CharField(
        max_length=3, choices=TIPO_RESPOSTA, verbose_name='Tipo de Resposta')
    referencia_resposta = models.ForeignKey(Referencia, related_name='referencia_resposta',
     on_delete=models.CASCADE, verbose_name='Referência Resposta')
    outras_referencias = models.ForeignKey(Referencia, related_name='outras_referencias',
     on_delete=models.CASCADE, verbose_name='Outras Referências')
    alternativas = models.ForeignKey(Alternativa, related_name='alternativas',
     on_delete=models.CASCADE)
    alternativas_corretas = models.ForeignKey(Alternativa, related_name='alternativas_corretas',
     on_delete=models.CASCADE, verbose_name='Alternativas Corretas')
    criado_por = models.ForeignKey(User, related_name='criado_por',
     on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    revisado_por = models.ForeignKey(User,related_name='revisado_por',
     on_delete=models.CASCADE)
    revisado_em = models.DateTimeField(auto_now_add=True)
    publicado_por = models.ForeignKey(User, related_name='publicado_por',
     on_delete=models.CASCADE)
    publicado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pergunta'
        verbose_name = 'Pergunta'


class Comentario(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    email = models.CharField(max_length=126)
    phone = models.CharField(max_length=11)
    is_whatsapp = models.BooleanField('É Whatsapp?', default=True)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comentario'
