import graphene as g
from .schema_nodes import *

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
        refencia_resposta_id = g.Int()
        outras_referencias = g.String()
        
    ok = g.Boolean()
    pergunta = g.Field(PerguntaNode)
    
    @classmethod
    def mutate(cls, root, info, tema_id, enunciado, tipo_resposta, alternativas=None, refencia_resposta_id=None, outras_referencias=None):
        tema = Tema.objects.get(id=tema_id)
        
        pergunta = Pergunta(
            tema=tema,
            enunciado=enunciado,
            tipo_resposta=tipo_resposta,
            # criado_por,
            # enviado_status=True,
        )
        if outras_referencias:
            pergunta.outras_referencias=outras_referencias
        if refencia_resposta_id:
            referencia = Referencia.objects.get(id=refencia_resposta_id)
            pergunta.refencia_resposta = referencia
            
        pergunta.save()
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