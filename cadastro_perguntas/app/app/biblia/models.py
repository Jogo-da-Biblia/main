from django.db import models


class Livro(models.Model):
    testamento = models.ForeignKey(
        'Testamento',
        related_name='livros',
        on_delete=models.CASCADE
    )

    posicao = models.IntegerField()
    nome = models.CharField(max_length=20)
    sigla = models.CharField(max_length=3)

    def __str__(self):
        return self.nome


class Testamento(models.Model):
    nome = models.CharField(max_length=17)

    def __str__(self):
        return self.nome


class Versiculo(models.Model):
    versao = models.ForeignKey(
        'Versao',
        related_name='versiculos',
        on_delete=models.CASCADE
    )

    livro = models.ForeignKey(
        'Livro',
        related_name='versiculos',
        on_delete=models.CASCADE
    )

    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    texto = models.TextField()

    def __str__(self):
        return (
            f"""{self.livro.nome},
            {self.versao.nome},
            {self.capitulo}:{self.versiculo}"""
        )

    class Meta:
        verbose_name = 'Versículo'


class Versao(models.Model):
    nome = models.CharField(max_length=33)
    sigla = models.CharField(max_length=4)

    class Meta:
        verbose_name = 'Versão'
        verbose_name_plural = "Versões"

    def __str__(self):
        return self.nome

class LivroCapituloNumeroVersiculos(models.Model):
    livro = models.ForeignKey(
        'Livro',
        related_name='livro_num_versiculos',
        on_delete=models.CASCADE
    )

    capitulo = models.IntegerField()
    nu_total_versiculos = models.IntegerField()

    class Meta:
        verbose_name = 'Total de Versículos por Capítulo de cada Livro'

