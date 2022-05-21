from django.db import models

from app.perguntas.models import Pergunta
from app.core.models import User


class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    email = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')
    phone = models.ForeignKey(
        User,
        to_field='phone',
        related_name='comentario_phone',
        on_delete=models.CASCADE
    )
    is_whatsapp = models.BooleanField('É Whatsapp?', default=True)
    mensagem = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mensagem} - {self.email}'

    class Meta:
        db_table = 'comentario'
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
