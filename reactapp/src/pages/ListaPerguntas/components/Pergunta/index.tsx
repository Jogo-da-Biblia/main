import React from "react";
import { IPergunta } from "types/pergunta";
import { Container } from "./styles";

const Pergunta: React.FC<{ data: IPergunta }> = ({ data }) => {

    const fullStatus = (str: string): string => {
        switch (str) {
            case "ENV":
                return "Enviado";
            case "REV":
                return "Revisado";
            case "PUB":
                return "Publicado";
            case "NEG":
                return "Negado";
            default:
                return str;
        }
    }

    return (
        <Container>
            <p>{data.enumciado}</p>
            <p>R: {data.resposta}</p>
            <p>Tipo: {data.tipoResposta}</p>
            <p className={`status status-${data.status.toLowerCase()}`} >{fullStatus(data.status)}</p>
        </Container>
    )
}

export default Pergunta;