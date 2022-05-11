from django.db import models


class Livro(models.Model):
    testamento = models.ForeignKey(
        'Testamento', related_name='livros', on_delete=models.CASCADE)
    posicao = models.IntegerField()
    # capitulos = models.IntegerField(default=1)
    nome = models.CharField(max_length=20)

    def __str__(self):
        self.nome


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

    def __str__(self):
        return f"{self.livro} {self.versao} {self.capitulo}:{self.versiculo}"

    class Meta:
        verbose_name = 'Versículo'


class Versao(models.Model):
    nome = models.CharField(max_length=33)

    class Meta:
        verbose_name = 'Versão'
        verbose_name_plural = "Versões"

    def __str__(self):
        return self.nome
