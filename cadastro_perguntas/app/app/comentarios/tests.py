from django.test import TestCase
import pytest


@pytest.mark.django_db
def test_deve_retornar_todas_as_perguntas(client, criar_dados_de_teste, usuario_admin, todas_perguntas):
    resultado = client.execute(
        todas_perguntas_query, context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert resultado == {'data': {'perguntas': [{'id': f'{todas_perguntas[0].id}', 'enunciado': f'{todas_perguntas[0].enunciado}'}, {
        'id': f'{todas_perguntas[1].id}', 'enunciado': f'{todas_perguntas[1].enunciado}'}]}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_retornar_todos_os_comentarios(client, criar_dados_de_teste, usuario_admin, todos_comentarios, todas_perguntas):
    resultado = client.execute(
        todos_comentarios_query, context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert resultado == {'data': {'comentarios': [{'id': f'{todos_comentarios[0].id}', 'mensagem': f'{todos_comentarios[0].mensagem}', 'email': f'{todos_comentarios[0].email}', 'phone': f'{todos_comentarios[0].phone}', 'pergunta': {'id': f'{todas_perguntas[0].id}', 'enunciado': f'{todas_perguntas[0].enunciado}'}}, {
        'id': f'{todos_comentarios[1].id}', 'mensagem': f'{todos_comentarios[1].mensagem}', 'email': f'{todos_comentarios[1].email}', 'phone': f'{todos_comentarios[1].phone}', 'pergunta': {'id': f'{todas_perguntas[1].id}', 'enunciado': f'{todas_perguntas[1].enunciado}'}}]}}
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_adicionar_novo_comentario(client, usuario_admin, criar_dados_de_teste, todas_perguntas):
    pergunta_id = todas_perguntas[0].id

    resultado = client.execute(adicionar_comentario_mutation, variables={
                               'perguntaId': pergunta_id}, context_value=UsuarioEmContexto(usuario=usuario_admin))
    comentario_mais_novo = Comentario.objects.last()
    assert resultado == {'data': OrderedDict([('adicionarComentario', {'comentario': {'phone': f'{comentario_mais_novo.phone}', 'isWhatsapp': comentario_mais_novo.is_whatsapp, 'email': f'{comentario_mais_novo.email}',
                                             'mensagem': f'{comentario_mais_novo.mensagem}', 'pergunta': {'id': f'{comentario_mais_novo.pergunta.id}', 'enunciado': f'{comentario_mais_novo.pergunta.enunciado}'}}})])}
    assert len(Comentario.objects.all()) == 3
    assert 'errors' not in resultado
