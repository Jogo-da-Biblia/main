from django.db import models
from django.db.models import ForeignKey

class Testamento(models.Model):
    nome = models.CharField()

    class Meta:
        db_table = 'testamento'

class Livro(models.Model):
    testamento = models.ForeignKey(Testamento)
    posicao = models.IntegerField()
    nome = models.CharField(max_length=20)

    class Meta:
        db_table = 'livro'

class Versao(models.Model):
    nome = models.CharField(max_length=33)

    class Meta:
        db_table = 'versao'

class Versiculo(models.Model):
    versao = models.ForeignKey(Versao)
    livro = models.ForeignKey(Livro)
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    texto = models.TextField()

class Grupo(models.Model):
    nome = models.CharField()
    cor = models.CharField(max_length=6)

class TipoResposta(models.Model):
    TIPO_RESPOSTA = [
        ('MES', 'MultiplaEscolha'),
        ('RCO', 'ReferenciaCompleta'),
        ('RLC', 'ReferenciaLivroCapitulo'),
        ('RES', 'RespostaSimples')
    ]
    tipo_resposta = models.CharField(
        max_length=3, choices=TIPO_RESPOSTA)

class Referencia(models.Model):
    livro = models.ForeignKey(Livro)
    versiculo = models.ForeignKey(Versiculo)

class DjangoUser(models.Model):
    nome = models.CharField()
    email = models.CharField()
    whatsapp = models.CharField()
    senha = models.CharField()
    # role = DjangouserRole

class Alternativa(models.Model):
    texto = models.TextField()

class Pergunta(models.Model):
    grupo = models.ForeignKey(Grupo)
    enunciado = models.TextField()
    # tipo_resposta = TipoResposta
    referencia_resposta = models.ForeignKey(Referencia)
    outras_referencias = models.ForeignKey(Referencia)
    alternativas = models.ForeignKey(Alternativa)
    alternativas_corretas = models.ForeignKey(Alternativa)
    # status = PerguntaStatus
    criado_por = models.ForeignKey(DjangoUser)
    criado_em = models.DateTimeField(auto_now_add=True)
    revisado_por = models.ForeignKey(DjangoUser)
    revisado_em = models.DateTimeField(auto_now_add=True)
    publicado_por = models.ForeignKey(DjangoUser)
    publicado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

class Comentario(models.Model):
    pergunta = models.ForeignKey(Pergunta)
    email = models.CharField()
    whatsapp = models.CharField()
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

# class Resposta(models.Model):
#     tipo_resposta

#     pass


# testamento = models.ForeignKey(
#         'Testamento', related_name='livros', on_delete=models.CASCADE)
#     posicao = models.IntegerField()
#     capitulos = models.IntegerField(default=1)
#     nome = models.CharField(max_length=20)
