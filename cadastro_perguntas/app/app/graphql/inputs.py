import graphene


class TemaInput(graphene.InputObjectType):
    nome = graphene.String(required=True, description="Nome do Tema")
    cor = graphene.String(required=True, description="Cor do Tema")


class AlternativaInput(graphene.InputObjectType):
    texto = graphene.String(required=True, description="Texto da alternativa")
    correta = graphene.Boolean(required=True, description="Se a alternativa é correta")


class EditarAlternativaInput(graphene.InputObjectType):
    alternativa_id = graphene.Int(required=True)
    novo_texto = graphene.String(required=True, description="Texto da alternativa")
    novo_correta = graphene.Boolean(
        required=True, description="Se a alternativa é correta"
    )


class TipoRespostaEnum(graphene.Enum):
    MES = ("MES",)
    RCO = ("RCO",)
    RLC = ("RLC",)
    RES = ("RES",)

    @property
    def description(self):
        if self == TipoRespostaEnum.MES:
            return "Múltipla Escolha"
        elif self == TipoRespostaEnum.RCO:
            return "Referência Completa"
        elif self == TipoRespostaEnum.RLC:
            return "Referência Livro-Capítulo"
        elif self == TipoRespostaEnum.RES:
            return "Resposta Simples"


class PerguntaInput(graphene.InputObjectType):
    enunciado = graphene.String(required=True, description="Texto da pergunta")
    tema_id = graphene.ID(required=True, description="Tema da pergunta")
    tipo_resposta = TipoRespostaEnum(required=True)
    referencia = graphene.String(
        required=True,
        description="Referência da pergunta e resposta correta para a pergunta",
    )
    referencia_biblica = graphene.Boolean(
        required=True,
        description="Se é uma referência biblica, caso seja uma referência externa o valor deve ser falso",
    )
    alternativas = graphene.List(
        AlternativaInput, required=True, description="Alternativas da pergunta"
    )


class UsuarioInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    name = graphene.String(required=True)
    phone = graphene.String(required=True)
    is_whatsapp = graphene.Boolean(required=True)
