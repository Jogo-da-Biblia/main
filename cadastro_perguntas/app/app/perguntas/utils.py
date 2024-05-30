import requests
from app.perguntas.models import Pergunta, Alternativa, Tema
from app.settings import GET_BIBLIA_VERSE_URL

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


def check_if_referencia_biblica_is_valid(referencia):
    params = {"q": referencia}
    response = requests.get(GET_BIBLIA_VERSE_URL, params=params)
    if response.status_code != 200:
        raise Exception(
            "Não foi possível encontrar a referência biblica, por favor adicionar uma única referencia"
        )
    return True
