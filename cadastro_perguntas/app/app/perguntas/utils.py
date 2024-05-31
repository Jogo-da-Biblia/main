import requests
from app.perguntas.models import Pergunta, Alternativa, Tema
from app.settings import GET_BIBLIA_VERSE_URL

from django.db import transaction, IntegrityError
from django.utils import timezone


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


def update_pergunta_values(new_fields, pergunta):
    try:
        with transaction.atomic():
            for key, value in new_fields.items():
                if value is not None:
                    if key == "tema":
                        value = Tema.objects.get(id=value)
                    elif key == "referencia":
                        if any(
                            [
                                new_fields["referencia_biblica"] is None
                                and pergunta.referencia_biblica is True,
                                new_fields["referencia_biblica"] is True,
                            ]
                        ):
                            check_if_referencia_biblica_is_valid(referencia=value)
                    elif key == "tipo_resposta":
                        value = value.name
                    elif key == "alternativas":
                        _update_alternativas_values(pergunta, value)
                        continue
                    setattr(pergunta, key, value)
        pergunta.save()
    except IntegrityError as e:
        raise Exception(
            f"Dados inválidos. Não foi possível atualizar a pergunta com os dados: {e}"
        )

    return


def _update_alternativas_values(pergunta, value):
    if len(value) == 0:
        return

    for nova_alternativa in value:
        alternativa = pergunta.alternativas.get(id=nova_alternativa.alternativa_id)

        new_alternativas_fields = {
            "texto": nova_alternativa.novo_texto,
            "correta": nova_alternativa.novo_correta,
        }

        for key, value in new_alternativas_fields.items():
            if value is not None:
                setattr(alternativa, key, value)

        alternativa.save()


def aprove_pergunta(user, pergunta):
    pergunta.aprovado_por = user
    pergunta.aprovado_em = timezone.now()
    pergunta.aprovado_status = True
    pergunta.recusado_status = False
    pergunta.save()

    return pergunta


def refuse_pergunta(user, pergunta):
    pergunta.recusado_por = user
    pergunta.recusado_em = timezone.now()
    pergunta.recusado_status = True
    pergunta.aprovado_status = False
    pergunta.publicado_status = False
    pergunta.save()

    return pergunta


def publish_pergunta(user, pergunta):
    pergunta.publicado_por = user
    pergunta.publicado_em = timezone.now()
    pergunta.publicado_status = True
    pergunta.save()

    return pergunta
