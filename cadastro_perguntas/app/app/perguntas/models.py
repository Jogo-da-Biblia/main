from app.biblia.models import Livro, Versiculo
from app.core.models import DjangoUser
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
        ('MES', 'MultiplaEscolha'),
        ('RCO', 'ReferenciaCompleta'),
        ('RLC', 'ReferenciaLivroCapitulo'),
        ('RES', 'RespostaSimples')
    ]
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    enunciado = models.TextField()
    tipo_resposta = models.CharField(
        max_length=3, choices=TIPO_RESPOSTA)
    referencia_resposta = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    outras_referencias = models.ForeignKey(Referencia, on_delete=models.CASCADE)
    alternativas = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    alternativas_corretas = models.ForeignKey(Alternativa, on_delete=models.CASCADE)
    criado_por = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    revisado_por = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    revisado_em = models.DateTimeField(auto_now_add=True)
    publicado_por = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    publicado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pergunta'


class Comentario(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    email = models.CharField(max_length=126)
    whatsapp = models.CharField(max_length=11)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'comentario'
