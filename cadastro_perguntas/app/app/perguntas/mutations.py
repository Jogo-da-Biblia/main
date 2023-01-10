import graphene as g
from .schema import *
import re

from .models import *


class CreateTema(g.Mutation):
    class Arguments:
        nome = g.String(required=True)
        cor = g.String(required=True)
        
    ok = g.Boolean()
    tema = g.Field(TemaNode)
    
    @classmethod
    def mutate(cls, root, info, nome, cor):
        tema = Tema(nome=nome, cor=cor)
        tema.save()
        ok = True
        return CreateTema(tema=tema, ok=ok)


class CreateReferencia(g.Mutation):
    class Arguments:
        livro_id = g.Int(required=True)
        versiculo_id = g.Int(required=True)
        
    ok = g.Boolean()
    referencia = g.Field(ReferenciaNode)
    
    @classmethod
    def mutate(cls, root, info, livro_id, versiculo_id):
        livro = Livro.objects.get(id=livro_id)
        versiculo = Versiculo.objects.get(id=versiculo_id)
        
        referencia = Tema(livro=livro, versiculo=versiculo)
        referencia.save()
        
        ok = True
        return CreateReferencia(referencia=referencia, ok=ok)


class CreatePergunta(g.Mutation):
    class Arguments:
        tema_id = g.Int(required=True)
        enunciado = g.String(required=True)
        tipo_resposta = g.String(required=True)
        alternativas = g.List(g.String)
        tipo_refencia = g.Int()
        refencia_regex = g.String()
        outras_referencias = g.String()
        
    ok = g.Boolean()
    pergunta = g.Field(PerguntaNode)
    
    @classmethod
    def mutate(cls, root, info, tema_id, enunciado, tipo_resposta, alternativas=None, refencia_regex=None, outras_referencias=None, tipo_refencia=1):
        
        user_ctx = info.context.user
        if user_ctx.is_anonymous:
            raise Exception('Not logged in!')
        
        tema = Tema.objects.get(id=tema_id)
        user = User.objects.get(pk=user_ctx.pk)
        
        pergunta = Pergunta(
            tema=tema,
            enunciado=enunciado,
            tipo_resposta=tipo_resposta,
            criado_por=user,
            # enviado_status=True,
        )
        
        if outras_referencias and tipo_refencia == 2:
            pergunta.outras_referencias=outras_referencias
            
        pergunta.save()
            
        if refencia_regex and tipo_refencia == 1:
          matches = refencia_regex.split(";")
          
          for m in matches:
            sigla = m.split(" ")[0]
            
            versiculos = re.findall(r"[\s,][\d]{1,2}:", m)
            capitulos = re.split("[^\d][\d]{1,2}:", "," + m.split(" ")[1])[1:]
        
            for i in range(len(capitulos)):
                capitulos[i] = capitulos[i].split(",")
        
            for i in range(len(capitulos)):
                for j in range(len(capitulos[i])):
                    regex_pattern = re.compile(r"[\d]{1,2}-[\d]{1,2}")
                    if regex_pattern.search(capitulos[i][j]):
                        cap_range = capitulos[i][j].split("-")
                        range_list = [num for num in range(int(cap_range[0]), int(cap_range[1]) + 1)]
                        
                        capitulos[i].pop(j)
                        
                        for n in range_list:
                            capitulos[i].append(str(n))
                        
            versiculos_n = [re.sub(r'[^\d]', "", v) for v in versiculos]                  
            
            for i in range(len(versiculos_n)):
                for c in capitulos[i]:
                    livro = Livro.objects.get(sigla=sigla)
                    versiculo = Versiculo.objects.get(versiculo=versiculos_n[i], capitulo=c)
    
                    referencia = Referencia(livro=livro, versiculo=versiculo, pergunta=pergunta)
                    referencia.save()
        
        if alternativas: 
            for alter in alternativas:
                alternativa = Alternativa(texto=alter.texto, pergunta=pergunta)
                alternativa.save()
        ok = True
        return CreatePergunta(pergunta=pergunta, ok=ok)


class CreateAlternativa(g.Mutation):
    class Arguments:
        texto = g.String(required=True)
        
    ok = g.Boolean()
    alternativa = g.Field(AlternativaNode)
    
    @classmethod
    def mutate(cls, root, info, texto):
        alternativa = Alternativa(texto=texto)
        alternativa.save()
        ok = True
        return CreateAlternativa(alternativa=alternativa, ok=ok)