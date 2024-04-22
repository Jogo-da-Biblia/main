import re
from app.biblia.models import Livro, Versao, Versiculo

TXT_BIBLICO_REGEX = r'^(\w+)\s+(\d+):(.*)$'

def get_texto_biblico(text_info: dict, version: Versao):
    textos = []
    livro = Livro.objects.get(sigla=text_info['livro'])
    try:
        current_versiculo = Versiculo.objects.get(livro_id=livro, versao_id=version, versiculo=text_info['versiculo'], capitulo=int(text_info['capitulo']))
        textos.append(current_versiculo)
    except Versiculo.DoesNotExist:
        raise Exception(f'O versiculo {text_info} nao existe na base de dados')

    return textos

def serialize_texto_biblico(referencia, version, todos_os_textos=None):
    if todos_os_textos is None:
        todos_os_textos = []
    for ref in referencia.split(';'):
        ref = ref.strip()
        if ref == '':
            continue
        # Adicionar um espaco depois de cada virgula
        ref = re.sub(r',\s*', ', ', ref)
        match = re.match(TXT_BIBLICO_REGEX, ref)
        versiculos_list = []
        if match:
            livro = match.group(1)
            capitulo = match.group(2)
            versiculos = match.group(3)
            for v in versiculos.split(','):
                if ':' in v:
                    todos_os_textos = serialize_texto_biblico(referencia=f'{livro}{v}', version=version, todos_os_textos=todos_os_textos)
                    continue
                elif '-' in v:
                    v = range(
                        int(v.split('-')[0]), int(v.split('-')[1])+1)
                    versiculos_list.extend(v)
                else:
                    versiculos_list.append(v)
            for versiculo in versiculos_list:
                todos_os_textos.append((str(livro), str(capitulo), str(versiculo)))

        else:
            raise Exception('Texto biblico no formato invalido')
    
    return todos_os_textos