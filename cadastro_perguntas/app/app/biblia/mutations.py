from graphene import Mutation, String, Int, Field, InputObjectType, Boolean
from .schema_nodes import *

from .models import Livro, Testamento, Versiculo, Versao

class LivroInputFields(InputObjectType):
    posicao = Int(required=True)
    nome = String(required=True)
    sigla = String(required=True)
    testamento = String(required=True)
    
    
class CreateLivroMutation(Mutation):
    class Arguments:
        data = LivroInputFields(required=True)
        
    # response
    ok = Boolean()
    livro = Field(LivroNode)
    
    @classmethod
    def mutate(cls, root, info, data):
        testamento = Testamento.objects.get(pk=data.testamento)
        livro = Livro.objects.create(
                posicao=data.posicao,
                nome=data.nome,
                sigla=data.sigla,
                testamento=testamento
            )
        livro.save()
        ok = True
        return CreateLivroMutation(livro=livro, ok=ok)
    
    
class UpdateLivroInputFields(InputObjectType):
    posicao = Int()
    nome = String()
    sigla = String()
    testamento = String()
    
    
class UpdateLivroMutation(Mutation):
    class Arguments:
        id = Int(required=True)
        data = LivroInputFields(required=True)
        
    ok = Boolean()
    livro = Field(LivroNode)
        
    @classmethod
    def mutate(cls, root, info, id, data):
        try:
            testamento = Testamento.objects.get(pk=data.testamento)
            livro = Livro.objects.get(pk=id)
            livro.posicao=data.posicao
            livro.nome=data.nome
            livro.sigla=data.sigla
            livro.testamento=testamento
            livro.save()
            ok = True
            return UpdateLivroMutation(livro=livro, ok=ok)
        except Livro.DoesNotExist:
            return None
        
    
class CreateTestamentoMutation(Mutation):
    class Arguments:
        nome = String(required=True)
        
    # response
    ok = Boolean()
    testamento = Field(TestamentoNode)
    
    @classmethod
    def mutate(cls, root, info, nome=None):
        testamento = Testamento.objects.create(nome=nome)
        testamento.save()
        ok = True
        return CreateTestamentoMutation(testamento=testamento, ok=ok)
    
    
class VersiculoInputFields(InputObjectType):
    capitulo = Int(required=True)
    versiculo = Int(required=True)
    texto = String(required=True)
    livro = String(required=True)
    
    
class CreateVersiculoMutation(Mutation):
    class Arguments:
        data = VersiculoInputFields(required=True)
        
    # response
    ok = Boolean()
    versiculo = Field(VersiculoNode)
    
    @classmethod
    def mutate(cls, root, info, data=None):
        livro = Livro.objects.get(pk=data.livro)
        versiculo = Versiculo.objects.create(
                capitulo=data.capitulo,
                versiculo=data.versiculo,
                texto=data.texto,
                livro=livro
            )
        versiculo.save()
        ok = True
        return CreateVersiculoMutation(versiculo=versiculo, ok=ok)
    
    
    
class CreateVersaoMutation(Mutation):
    class Arguments:
        nome = String(required=True)
        
    # response
    ok = Boolean()
    versao = Field(VersaoNode)
    
    @classmethod
    def mutate(cls, root, info, nome=None):
        versao = Versao.objects.create(nome=nome)
        versao.save()
        ok = True
        return CreateVersaoMutation(versao=versao, ok=ok)