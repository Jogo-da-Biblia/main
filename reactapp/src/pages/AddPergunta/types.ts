import { IAlternativa } from "global/types/pergunta";

export interface IReferencia {
    regex: string;
    textual: string;
}

export interface IAddPergunta {
    tema: number;
    enumciado: string;
    tipoResposta: number;
    referencia: IReferencia;
    tipoReferencia: number;
    alternativas: IAlternativa[]
}