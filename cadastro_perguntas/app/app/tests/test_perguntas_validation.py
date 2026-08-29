from types import SimpleNamespace

import pytest

from app.perguntas.utils import (
    check_if_referencia_biblica_is_valid,
    validate_bible_reference_syntax,
    validate_question_answers,
)


def answer(correta, texto="Resposta"):
    return SimpleNamespace(correta=correta, texto=texto)


def test_referencia_livro_capitulo_nao_aceita_versiculo():
    assert validate_bible_reference_syntax("2 Reis 22", "RLC") == (
        "2 Reis 22",
        "2 Reis 22:1",
    )
    with pytest.raises(ValueError, match="não informe versículos"):
        validate_bible_reference_syntax("2 Reis 22:1", "RLC")
    assert validate_bible_reference_syntax("2 Reis 22; João 3", "RLC") == (
        "2 Reis 22; João 3",
        "2 Reis 22:1; João 3:1",
    )


def test_referencia_completa_exige_versiculo_e_aceita_varias_referencias():
    assert validate_bible_reference_syntax("João 3:16-18", "RCO") == (
        "João 3:16-18",
        "João 3:16-18",
    )
    with pytest.raises(ValueError, match="Faltou o versículo"):
        validate_bible_reference_syntax("João 3", "RCO")
    assert validate_bible_reference_syntax(
        "João 3:16; Mateus 5:1", "RCO"
    ) == (
        "João 3:16; Mateus 5:1",
        "João 3:16; Mateus 5:1",
    )


def test_lista_identifica_qual_referencia_contem_erro():
    with pytest.raises(ValueError, match="Referência 2"):
        validate_bible_reference_syntax("João 3:16; Mateus 5", "RCO")


def test_multipla_escolha_aceita_mais_de_uma_alternativa_correta():
    validate_question_answers(
        "MES",
        [answer(True, "Oito anos"), answer(True, "8 anos"), answer(False, "25 anos")],
    )


def test_multipla_escolha_exige_duas_alternativas_e_uma_correta():
    with pytest.raises(ValueError, match="pelo menos duas"):
        validate_question_answers("MES", [answer(True)])
    with pytest.raises(ValueError, match="pelo menos uma alternativa"):
        validate_question_answers("MES", [answer(False, "A"), answer(False, "B")])


def test_resposta_simples_aceita_varias_formas_corretas():
    validate_question_answers("RES", [answer(True, "Josias"), answer(True, "Rei Josias")])
    with pytest.raises(ValueError, match="pelo menos uma resposta simples"):
        validate_question_answers("RES", [])
    with pytest.raises(ValueError, match="devem ser aceitas"):
        validate_question_answers("RES", [answer(True, "Josias"), answer(False, "Outro")])


def test_respostas_nao_podem_ser_vazias_ou_repetidas():
    with pytest.raises(ValueError, match="não podem ficar em branco"):
        validate_question_answers("MES", [answer(True, "A"), answer(False, "  ")])
    with pytest.raises(ValueError, match="não pode ser adicionada duas vezes"):
        validate_question_answers("RES", [answer(True, "Josias"), answer(True, "josias")])


def test_servico_informa_quando_capitulo_ou_versiculo_nao_existe(monkeypatch):
    response = SimpleNamespace(
        status_code=200,
        json=lambda: [{"texto": "Versículo Jo 999:1 não encontrado na versão ARA"}],
    )
    monkeypatch.setattr("app.perguntas.utils.requests.get", lambda *args, **kwargs: response)

    with pytest.raises(ValueError, match="capítulo ou versículo não existe"):
        check_if_referencia_biblica_is_valid("João 999:1", "RCO")
