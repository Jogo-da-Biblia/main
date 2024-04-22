from django.test import TestCase
import pytest

@pytest.mark.parametrize('tipo_resposta', ['MES', 'RCO', 'RLC', 'RES'])
@pytest.mark.django_db
def test_deve_adicionar_nova_pergunta(client, usuario_admin, criar_dados_de_teste, tipo_resposta):
    tema_id = Tema.objects.get(nome='Doutrina').id
    referencia_id = Referencia.objects.all()[0].id
    
    resultado = client.execute(adicionar_nova_pergunta_mutation, variables={'temaId': tema_id, 'referenciaId': referencia_id, 'tipoResposta': tipo_resposta}, context_value=UsuarioEmContexto(usuario=usuario_admin))
    
    pergunta_mais_nova = Pergunta.objects.last()
    assert resultado == {'data': OrderedDict([('cadastrarPergunta', {'pergunta': {'id': f'{pergunta_mais_nova.id}', 'tema': {'nome': f'{pergunta_mais_nova.tema.nome}'}, 'enunciado': f'{pergunta_mais_nova.enunciado}', 'tipoResposta': f'{pergunta_mais_nova.tipo_resposta}', 'status': pergunta_mais_nova.status, 'revisadoPor': None}})])}
    assert len(Pergunta.objects.all()) == 3
    assert 'errors' not in resultado


@pytest.mark.django_db
def test_deve_editar_nova_pergunta(client, usuario_admin, criar_dados_de_teste):
    nova_pergunta = Pergunta.objects.create(
        tema = Tema.objects.get(nome='Doutrina'),
        enunciado = 'enunciado1adadasdasda',
        tipo_resposta = 'MES',
        criado_por = usuario_admin,
        status=False
    )
    pergunta_id = nova_pergunta.id

    assert nova_pergunta.enunciado == 'enunciado1adadasdasda'
    assert nova_pergunta.status == False

    tema_id = Tema.objects.get(nome='Doutrina').id
    referencia_id = Referencia.objects.all()[0].id


    resultado = client.execute(editar_pergunta_mutation, variables={'temaId': tema_id, 'referenciaId': referencia_id, 'perguntaId': pergunta_id}, context_value=UsuarioEmContexto(usuario=usuario_admin))
    nova_pergunta.refresh_from_db()

    assert resultado == {'data': OrderedDict([('editarPergunta', {'pergunta': {'id': f'{nova_pergunta.id}', 'enunciado': 'Novo enunciado', 'revisadoPor': None, 'status': True}})])}
    assert nova_pergunta.enunciado == 'Novo enunciado'
    assert nova_pergunta.status == True
    assert 'errors' not in resultado

@pytest.mark.django_db
def test_deve_retornar_pergunta_aleatoria_de_um_tema(client, criar_dados_de_teste, usuario_admin):
    tema_id = Tema.objects.get(nome='Conhecimentos Gerais').id
    # So tem uma pergunta no tema Conhecimentos Gerais para testes
    pergunta_conhecimentos_gerais = Pergunta.objects.get(tema=tema_id)
    resultado = client.execute(pergunta_aleatoria_query, variables={'temaId': tema_id}, context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert resultado == {'data': {'pergunta': [{'id': f'{pergunta_conhecimentos_gerais.id}', 'enunciado': f'{pergunta_conhecimentos_gerais.enunciado}'}]}}
    assert 'errors' not in resultado
