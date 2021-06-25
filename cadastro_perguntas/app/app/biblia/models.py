from django.db import models


class Livro(models.Model):
    testamento = models.ForeignKey(
        'Testamento', related_name='livros', on_delete=models.CASCADE)
    posicao = models.IntegerField()
    # capitulos = models.IntegerField(default=1)
    nome = models.CharField(max_length=20)


class Testamento(models.Model):
    nome = models.CharField(max_length=17)


class Versiculo(models.Model):
    versao = models.ForeignKey(
        'Versao', related_name='versiculos', on_delete=models.CASCADE)
    livro = models.ForeignKey(
        'Livro', related_name='versiculos', on_delete=models.CASCADE)
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    texto = models.TextField()


class Versao(models.Model):
    nome = models.CharField(max_length=33)

    class Meta:
        verbose_name_plural = "versoes"
