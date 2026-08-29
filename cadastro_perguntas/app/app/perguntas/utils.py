import re

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


BOOK_AND_CHAPTER_PATTERN = re.compile(
    r"^(?P<book>[A-Za-z\s\u00C0-\u017F0-9]+?)\s+(?P<chapter>\d+)$"
)
COMPLETE_REFERENCE_PATTERN = re.compile(
    r"^(?P<book>[A-Za-z\s\u00C0-\u017F0-9]+?)\s+(?P<chapter>\d+):(?P<verses>.+)$"
)


def _positive_number(value, label):
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} deve ser um número maior que zero.") from error
    if number < 1:
        raise ValueError(f"{label} deve ser um número maior que zero.")
    return number


def _validate_verse_part(part):
    if ":" in part:
        chapter, verse_expression = part.split(":", 1)
        _positive_number(chapter, "O capítulo")
    else:
        verse_expression = part

    if not re.fullmatch(r"\d+(?:-\d+)?", verse_expression):
        raise ValueError(
            f'O trecho "{part}" não é um versículo ou uma faixa válida.'
        )

    limits = verse_expression.split("-", 1)
    start = _positive_number(limits[0], "O versículo")
    if len(limits) == 2:
        end = _positive_number(limits[1], "O fim da faixa de versículos")
        if start > end:
            raise ValueError(
                "A faixa de versículos deve começar pelo menor número."
            )


def _validate_single_bible_reference_syntax(referencia, tipo_resposta):
    referencia = " ".join((referencia or "").strip().split())
    if not referencia:
        raise ValueError("Informe a referência bíblica.")

    if tipo_resposta == "RLC":
        if ":" in referencia:
            raise ValueError(
                "Para livro e capítulo, não informe versículos. Exemplo: 2 Reis 22."
            )
        match = BOOK_AND_CHAPTER_PATTERN.fullmatch(referencia)
        if match is None:
            raise ValueError(
                "Informe o livro seguido do capítulo. Exemplo: 2 Reis 22."
            )
        _positive_number(match.group("chapter"), "O capítulo")
        return referencia, f"{referencia}:1"

    match = COMPLETE_REFERENCE_PATTERN.fullmatch(referencia)
    if match is None:
        if BOOK_AND_CHAPTER_PATTERN.fullmatch(referencia):
            raise ValueError(
                "Faltou o versículo. Use dois-pontos depois do capítulo, como em João 3:16."
            )
        raise ValueError(
            "Informe livro, capítulo e versículo. Exemplo: João 3:16."
        )

    _positive_number(match.group("chapter"), "O capítulo")
    verse_parts = [part.strip() for part in match.group("verses").split(",")]
    if any(not part for part in verse_parts):
        raise ValueError("Há um versículo vazio depois da vírgula.")
    for part in verse_parts:
        _validate_verse_part(part)

    normalized = re.sub(r",\s*", ", ", referencia)
    return normalized, normalized


def validate_bible_reference_syntax(referencia, tipo_resposta):
    referencia = (referencia or "").strip()
    if not referencia:
        raise ValueError("Informe a referência bíblica.")

    raw_references = [item.strip() for item in referencia.split(";")]
    for index, raw_reference in enumerate(raw_references):
        if not raw_reference:
            raise ValueError(
                f"A referência {index + 1} está vazia. Remova o ponto e vírgula excedente ou informe a passagem."
            )

    normalized_references = []
    lookup_references = []
    for index, raw_reference in enumerate(raw_references):
        try:
            normalized, lookup = _validate_single_bible_reference_syntax(
                raw_reference, tipo_resposta
            )
        except ValueError as error:
            if len(raw_references) == 1:
                raise
            raise ValueError(
                f'Referência {index + 1} ("{raw_reference}"): {error}'
            ) from error
        normalized_references.append(normalized)
        lookup_references.append(lookup)

    return "; ".join(normalized_references), "; ".join(lookup_references)


def validate_question_answers(tipo_resposta, alternativas):
    alternativas = alternativas or []
    if any(not (alternativa.texto or "").strip() for alternativa in alternativas):
        raise ValueError("Alternativas e respostas simples não podem ficar em branco.")
    normalized_answers = [
        alternativa.texto.strip().casefold() for alternativa in alternativas
    ]
    if len(normalized_answers) != len(set(normalized_answers)):
        raise ValueError("A mesma alternativa ou resposta não pode ser adicionada duas vezes.")
    if tipo_resposta == "MES":
        if len(alternativas) < 2:
            raise ValueError("Adicione pelo menos duas alternativas.")
        if not any(alternativa.correta for alternativa in alternativas):
            raise ValueError("Marque pelo menos uma alternativa como correta.")
    elif tipo_resposta == "RES":
        if not alternativas:
            raise ValueError("Adicione pelo menos uma resposta simples aceita.")
        if any(not alternativa.correta for alternativa in alternativas):
            raise ValueError(
                "Todas as respostas simples cadastradas devem ser aceitas como corretas."
            )
    elif alternativas:
        raise ValueError(
            "Perguntas de referência usam a própria referência como resposta e não recebem alternativas."
        )


def check_if_referencia_biblica_is_valid(referencia, tipo_resposta=None):
    if tipo_resposta is None:
        normalized_reference = (referencia or "").strip()
        lookup_reference = normalized_reference
    else:
        normalized_reference, lookup_reference = validate_bible_reference_syntax(
            referencia=referencia, tipo_resposta=tipo_resposta
        )
    params = {"q": lookup_reference}
    try:
        response = requests.get(GET_BIBLIA_VERSE_URL, params=params, timeout=10)
    except requests.RequestException as error:
        raise Exception(
            "Não foi possível conferir a referência bíblica agora. Tente novamente."
        ) from error
    if response.status_code != 200:
        raise ValueError(
            "A referência tem formato válido, mas o livro, capítulo ou versículo não foi encontrado."
        )
    try:
        verses = response.json()
    except (TypeError, ValueError) as error:
        raise ValueError(
            "O serviço da Bíblia retornou uma resposta inválida para a referência."
        ) from error
    if not isinstance(verses, list) or not verses:
        raise ValueError("Nenhum versículo foi encontrado para essa referência.")
    if any(
        re.search(r"não encontrado|erro ao recuperar", verse.get("texto", ""), re.I)
        for verse in verses
        if isinstance(verse, dict)
    ):
        raise ValueError(
            "O livro foi reconhecido, mas o capítulo ou versículo não existe."
        )
    return normalized_reference


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
