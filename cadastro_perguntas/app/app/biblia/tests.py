from django.test import TestCase

@pytest.mark.parametrize('texto_biblico_referencia', [('Gn 1:26', 1), ('Gn 1:26-28', 3), ('Gn 1:26,28', 2), ('Gn 1:26-28,31', 4), ('Gn 1:27-29, 2:1', 4), ('Gn 1:27,28,31, 2:1', 4), ('Gn 1:26-28,31, 2:1; Mt 1:1-3', 8), ('Gn 1:26-28,31,2:1; Mt 1:1,2, 1:3', 8), ('Gn 1:26-28,31, 2:1; Mt 1:1-3; Gl 2:20', 9)])
@pytest.mark.django_db
def test_deve_buscar_texto_biblico(client, usuario_admin, criar_dados_de_teste, texto_biblico_referencia):
    texto_biblico, quant_esperada_versiculos = texto_biblico_referencia

    resultado = client.execute(texto_biblico_query, variables={'textoBiblicoReferencia': texto_biblico},context_value=UsuarioEmContexto(usuario=usuario_admin))

    assert len(resultado['data']['textoBiblico']) == quant_esperada_versiculos
    assert 'errors' not in resultado
    assert 'None' not in resultado
