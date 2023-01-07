export interface IPergunta {
    id: string;
    enumciado: string;
    resposta: string;
    tipoResposta: string;
    status: "ENV" | "REV" | "PUB" | "NEG";
}

export interface IAlternativa {
    texto: string;
    alternativaCorreta: boolean
}
