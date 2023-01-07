import React, { useState } from "react";
import { Button } from "global/styles/globalStyles";
import { IAlternativa } from "global/types/pergunta";
import TextArea from "../TextArea";
import AlternativaDetail from "./components/AlternativaDetail";

interface IAlternativaProps {
    alternativas?: IAlternativa[];
    addAlternativa: (alt: IAlternativa) => void;
    removerAlternativa: (i: number) => void;
    setAlternativaCorreta: (i: number) => void;
}

const RespostaSimples: React.FC<IAlternativaProps> = (props) => {
    const [text, setText] = useState("")

    const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setText(e.target.value)
    }

    const handleClick = () => {
        props.addAlternativa({
            texto: text,
            alternativaCorreta: false,
        })
        setText("")
    }

    return (
        <>
            <h2>Adicionar alternativas</h2>
            <TextArea name="" id="" value={text} onChange={handleChange} />
            <Button type="button" onClick={handleClick} disabled={!text} children="Adicionar alternativa" />
            {props.alternativas && props.alternativas.map((alt, i) => (
                <AlternativaDetail 
                key={i} 
                setAlternativaCorreta={props.setAlternativaCorreta} 
                removerAlternativa={props.removerAlternativa} 
                index={i} 
                alt={alt} />
            ))}
        </>
    )
}

export default RespostaSimples