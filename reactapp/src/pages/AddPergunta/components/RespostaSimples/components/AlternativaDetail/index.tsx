import { CheckboxLabel } from "pages/AddPergunta/styles";
import React from "react";
import { Checkmark } from "styles/globalStyles";
import { IAlternativa } from "types/pergunta";
import { AlternativaLabel, Container, Controls, DeleteBtn } from "./styles";
import lixeiraIcon from "assets/lixeira.png"

interface IAlternativaDetailProps {
    alt: IAlternativa;
    index: number;
    setAlternativaCorreta: (i: number) => void
    removerAlternativa: (i: number) => void
}

const AlternativaDetail: React.FC<IAlternativaDetailProps> = (props) => {
    return (
        <Container>
            {props.alt.texto}
            <Controls>
                <CheckboxLabel >
                    <AlternativaLabel
                        correta={props.alt.alternativaCorreta}
                    >
                        Alternativa correta
                    </AlternativaLabel>
                    <input
                        type="checkbox"
                        onChange={() => props.setAlternativaCorreta(props.index)}
                        checked={props.alt.alternativaCorreta}
                    />
                    <Checkmark />
                </CheckboxLabel>
                <DeleteBtn type="button" onClick={() => props.removerAlternativa(props.index)}>
                    <img src={lixeiraIcon} alt="icone de lixeira" />
                </DeleteBtn>
            </Controls>

        </Container>
    )
}

export default AlternativaDetail;