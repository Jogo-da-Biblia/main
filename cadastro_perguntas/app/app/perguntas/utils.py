from app.perguntas.models import Pergunta, Alternativa, Tema

from django.db import transaction, IntegrityError


def criar_nova_pergunta_via_mutation(nova_pergunta, user):
    tema = Tema.objects.get(id=nova_pergunta.tema_id)

    try:
        with transaction.atomic():
            pergunta = Pergunta.objects.create(
                tema=tema,
                enunciado=nova_pergunta.enunciado,
                tipo_resposta=nova_pergunta.tipo_resposta.name,
                referencia=nova_pergunta.referencia,
                referencia_biblica=nova_pergunta.referencia_biblica,
                criado_por=user,
            )

            for alternativa in nova_pergunta.alternativas:
                Alternativa.objects.create(
                    pergunta=pergunta,
                    texto=alternativa.texto,
                    correta=alternativa.correta,
                )

            return pergunta
    except IntegrityError as e:
        raise Exception(
            f"Dados inválidos. Não foi possível criar a pergunta com os dados: {e}"
        )
