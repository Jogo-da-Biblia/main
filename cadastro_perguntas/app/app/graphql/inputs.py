import graphene


class AlternativaInput(graphene.InputObjectType):
    alternativa = graphene.String(
        required=True, description="Texto da alternativa")
    correta = graphene.Boolean(
        required=True, description="Se a alternativa é correta")


class PerguntaInput(graphene.InputObjectType):
    enunciado = graphene.String(required=True, description="Texto da pergunta")
    tema_id = graphene.ID(required=True, description="Tema da pergunta")
    # TODO: Implementar ENUM https://docs.graphene-python.org/en/latest/types/enums/
    tipo_resposta = graphene.String(
        required=True, description="Tipo de resposta da pergunta")
    referencia = graphene.String(
        required=True, description="Referência da pergunta e resposta correta para a pergunta")
    referencia_biblica = graphene.Boolean(
        required=True, description="Se é uma referência biblica, caso seja uma referência externa o valor deve ser falso")
    alternativas = graphene.List(
        AlternativaInput, required=True, description="Alternativas da pergunta")
