import { CheckboxLabel } from "pages/AddPergunta/styles";
import React from "react";
import { Checkmark } from "styles/globalStyles";
import { IReferencia } from "types/pergunta";
import TextArea from "../TextArea";
import { referenciaData } from "./data";
import { Container } from "./styles";

interface IReferenciaProps {
    mainValue: IReferencia
    tipoReferencta: number
    setReferencia: (k: string, v: string) => void
    setTipo: (k: string, v: number) => void
}

const Referencia: React.FC<IReferenciaProps> = ({ mainValue, tipoReferencta, setReferencia, setTipo }) => {

    const handleChangeRef = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setReferencia(e.target.name, e.target.value)
    }

    return (
        <Container>
            <h2>Referência</h2>
            {referenciaData.map((op, i) => (
                <CheckboxLabel key={i} >
                    <p>{op.label}</p>
                    <input type="checkbox" onChange={() => setTipo("tipoReferencia", op.value)} checked={op.value === tipoReferencta} />
                    <Checkmark spanHidden borderRadius="50%" />
                </CheckboxLabel>
            ))}
            <p className="op1-inf">
                Perguntas sobre a história da Igreja ou da Bíblia devem ter referência de onde foi extraído segundo o método de referência Vancouver
            </p>
            {
                tipoReferencta === 1 && (
                    <TextArea
                        id="referencia-regex"
                        name="regex"
                        value={mainValue.regex}
                        placeholder="Ex.: Gn 1:26"
                        onChange={handleChangeRef}
                    />
                )
            }
            {
                tipoReferencta === 2 && (
                    <TextArea
                        id="referencia-text"
                        name="textual"
                        value={mainValue.textual}
                        placeholder="Digite sua referência aqui"
                        onChange={handleChangeRef}
                    />
                )
            }
        </Container>
    )
}

export default Referencia;