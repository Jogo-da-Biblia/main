import { useState } from "react";
import { IAddPergunta, IAlternativa } from "types/pergunta";
import Alternativa from "./components/Alternativa";
import TextArea from "./components/TextArea";
import TipoResposta from "./components/TipoResposta";
import { Container, Form } from "./styles";

/*
pergunta = {
    tema: 1,
    enumciado: "",
    tipoResposta: 1,
    alternativas = [
        {
            texto: "",
            alternativaCorreta: false
        },
        {
            texto: "",
            alternativaCorreta: false
        },
        {
            texto: "",
            alternativaCorreta: true
        },
    ]
}
*/

const selectOptions = [
    { value: 1, label: "tema 1", },
    { value: 2, label: "tema 2", },
    { value: 3, label: "tema 3", },
    { value: 4, label: "tema 4", },
]

function AddPergunta() {
    const [data, setData] = useState<IAddPergunta>({
        tema: 1,
        enumciado: "",
        tipoResposta: 1
    })

    const setDataByKey = (name: string, value: any) => {
        setData(prev => ({
            ...prev,
            [name]: value
        }))
    }

    const handleChangeEnunciado = (e: React.ChangeEvent<HTMLTextAreaElement>) => setDataByKey("enumciado", e.target.value)

    const handleChangeTipoResposta = (value: number) => setDataByKey("tipoResposta", value)

    const addAlternativa = (alt: IAlternativa) => {
        const newArray = data.alternativas || []
        newArray.push(alt)
        setDataByKey("alternativas", newArray)
    }

    const setAlternativaCorreta = (index: number) => {
        if (!data.alternativas) return;
        const newArray = data.alternativas.map((alt, i) => ({ ...alt, alternativaCorreta: i === index ? true : false }))
        setDataByKey("alternativas", newArray)
    }

    const removerAlternativa = (index: number) => {
        if (!data.alternativas) return;
        const newArray = data.alternativas.filter((alt, i) => i !== index)
        setDataByKey("alternativas", newArray)
    }

    return (
        <Container>
            <h1>Adicionar Pergunta</h1>
            <p>Para começar a colaborar cadastre-se com seus dados abaixo e comece a enviar perguntas.</p>
            <Form>
                <select name="tema" id="tema">
                    {selectOptions.map(op => (
                        <option value={op.value}>{op.label}</option>
                    ))}
                </select>
                <TextArea name="" id="enumciado" value={data.enumciado} onChange={handleChangeEnunciado} />
                <TipoResposta mainValue={data.tipoResposta} setData={handleChangeTipoResposta} />
                {data.tipoResposta === 1 && (
                    <Alternativa
                        alternativas={data.alternativas}
                        addAlternativa={addAlternativa}
                        removerAlternativa={removerAlternativa}
                        setAlternativaCorreta={setAlternativaCorreta}
                    />
                )}
            </Form>
        </Container>
    )
}

export default AddPergunta