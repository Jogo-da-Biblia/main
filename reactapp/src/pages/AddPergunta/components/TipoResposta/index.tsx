import { CheckboxLabel } from "pages/AddPergunta/styles";
import React from "react";
import { Checkmark } from "global/styles/globalStyles";
import { tipoRespostaData } from "./data";
import { Container } from "./styles";

interface ITipoResposta {
    mainValue: number;
    setData: (value: number) => void
}

const TipoResposta: React.FC<ITipoResposta> = ({ mainValue, setData }) => {

    const handleChange = (value: number) => {
        setData(value)
    }

    return (
        <Container>
            <h2>Tipo de Resposta</h2>
            {tipoRespostaData.map((op, i) => (
                <CheckboxLabel key={i} >
                    <p>{op.label}</p>
                    <input type="checkbox" onChange={() => handleChange(op.value)} checked={op.value === mainValue} />
                    <Checkmark spanHidden borderRadius="50%" />
                </CheckboxLabel>
            ))}
        </Container>
    )
}

export default TipoResposta

