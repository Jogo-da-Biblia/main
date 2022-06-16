from django.db import models

from app.perguntas.models import Pergunta


class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    email = models.CharField(max_length=126)
    phone = models.CharField(max_length=11)
    is_whatsapp = models.BooleanField('É Whatsapp?', default=True)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mensagem} - {self.email}'

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
