from django.db import models


class Livro(models.Model):
    posicao = models.IntegerField()
    nome = models.CharField(max_length=20)
    sigla = models.CharField(max_length=20)
    testamento = models.ForeignKey(
        'Testamento',
        related_name='livros',
        on_delete=models.CASCADE
    ) 

    def __str__(self):
        return self.nome


class Testamento(models.Model):
    nome = models.CharField(max_length=17)

    def __str__(self):
        return self.nome


class Versiculo(models.Model):
    capitulo = models.IntegerField()
    versiculo = models.IntegerField()
    texto = models.TextField()
    livro = models.ForeignKey(
        'Livro',
        related_name='versiculos',
        on_delete=models.CASCADE
    )
    versao = models.ForeignKey(
        'Versao',
        related_name='versiculos',
        on_delete=models.CASCADE
    )

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

    class Meta:
        verbose_name = 'Versão'
        verbose_name_plural = "Versões"

    def __str__(self):
        return self.nome


class TotalVersiculo(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    capitulo = models.IntegerField(default=1)
    nu_total_versiculos = models.IntegerField(default=1)
    
    def __str__(self):
        return "livro: {}, capitulo: {}, total_versículos: {}".format(self.livro, self.capitulo, self.nu_total_versiculos)