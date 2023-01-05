import SelectField from "components/Select";
import { FormEvent, useState, useEffect } from "react";
import { IAddPergunta, IAlternativa, IReferencia } from "types/pergunta";
import Alternativa from "./components/Alternativa";
import Referencia from "./components/Referencia";
import RespostaSimples from "./components/RespostaSimples";
import TextArea from "./components/TextArea";
import TipoResposta from "./components/TipoResposta";
import { Container, Form, SubmitBtn } from "./styles";
import { useQuery } from 'graphql-hooks'

// temp
const selectOptions = [
    { id: 1, name: "tema 1", },
    { id: 2, name: "tema 2", },
    { id: 3, name: "tema 3", },
    { id: 4, name: "tema 4", },
]

const TEMAS_QUERY = `query {
    temas {
      edges {
        node {
          nome
          cor
        }
      }
    }
  }`

function AddPergunta() {
    const { loading, error, data } = useQuery(TEMAS_QUERY, { errorPolicy: "all" })

    useEffect(() => {
        console.log(data);
        
    }, [])

    useEffect(() => {
        console.log(data);

    }, [])

    const [perguntaData, setData] = useState<IAddPergunta>({
        tema: 1,
        enumciado: "",
        tipoResposta: 1,
        alternativas: [],
        referencia: {
            regex: "",
            textual: ""
        },
        tipoReferencia: 1,
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
        const newArray = perguntaData.alternativas || []
        newArray.push(alt)
        setDataByKey("alternativas", newArray)
    }

    const setAlternativaCorreta = (index: number, single?: boolean) => {
        if (!perguntaData.alternativas) return;

        let newArray: IAlternativa[]

        if (single) {
            newArray = perguntaData.alternativas.map((alt, i) => ({ ...alt, alternativaCorreta: i === index }))
        } else {
            newArray = perguntaData.alternativas.map((alt, i) => ({
                ...alt,
                alternativaCorreta: i === index ? !alt.alternativaCorreta : alt.alternativaCorreta
            }))
        }

        setDataByKey("alternativas", newArray)
    }

    const removerAlternativa = (index: number) => {
        if (!perguntaData.alternativas) return;
        const newArray = perguntaData.alternativas.filter((alt, i) => i !== index)
        setDataByKey("alternativas", newArray)
    }

    const setReferencia = (key: string, value: string) => {
        let tempRef: IReferencia = perguntaData.referencia
        tempRef[key as keyof typeof tempRef] = value
        setDataByKey("referencia", tempRef)
    }

    const onSubmit = (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        let mandatoryData = ['Tema', 'Enumciado']

        let emptyField: {
            fields: string[],
            empty: boolean
        } = {
            fields: [],
            empty: false
        }

        mandatoryData.forEach((mandatory) => {
            if (perguntaData[mandatory.toLowerCase() as keyof IAddPergunta] === "") {
                emptyField.fields.push(mandatory)
                emptyField.empty = true
            }
        })

        if (emptyField.empty) return alert(`Campos [ ${emptyField.fields.join(", ")} ] não podem estar vazios`);

        const checkRange = (v: number, min: number, max: number) => {
            return !((v - min) * (v - max) <= 0);
        }

        switch (perguntaData.tipoResposta) {
            case 1:
                if (perguntaData.alternativas.length < 2) return alert("Deve haver mais de 1 alternativa");
                if (checkRange(perguntaData.alternativas.filter(alt => alt.alternativaCorreta === true).length, 1, 1))
                    return alert("Deve haver uma alternativa correta");
                break;
            case 4:
                if (perguntaData.alternativas.length < 2) return alert("Deve haver mais de 1 alternativa")
                if (!perguntaData.alternativas.some(alt => alt.alternativaCorreta === true)) return alert("Deve haver pelo menos uma alternativa correta")
                break;
        }
        // Se "referencia completa" -> Referencia (regex completo)
        // Se "referencia livro-capitulo" -> Referencia (regex livro-capitulo)

        switch (perguntaData.tipoReferencia) {
            case 1:
                if (!perguntaData.referencia.regex) return alert("Nenhuma referência bíblica digitada")
                break
            case 2:
                if (!perguntaData.referencia.textual) return alert("Nenhuma referência textual digitada")
        }

        console.log(perguntaData)
    }

    return (
        <Container>
            <h1>Adicionar Pergunta</h1>
            <p>Para começar a colaborar cadastre-se com seus dados abaixo e comece a enviar perguntas.</p>
            <Form onSubmit={onSubmit}>
                <SelectField array={selectOptions} />
                <TextArea name="" id="enumciado" value={perguntaData.enumciado} onChange={handleChangeEnunciado} />
                <TipoResposta mainValue={perguntaData.tipoResposta} setData={handleChangeTipoResposta} />
                {perguntaData.tipoResposta === 1 && (
                    <Alternativa
                        alternativas={perguntaData.alternativas}
                        addAlternativa={addAlternativa}
                        removerAlternativa={removerAlternativa}
                        setAlternativaCorreta={setAlternativaCorreta}
                    />
                )}
                {perguntaData.tipoResposta === 4 && (
                    <RespostaSimples
                        alternativas={perguntaData.alternativas}
                        addAlternativa={addAlternativa}
                        removerAlternativa={removerAlternativa}
                        setAlternativaCorreta={setAlternativaCorreta}
                    />
                )}
                <Referencia
                    mainValue={perguntaData.referencia}
                    tipoReferencta={perguntaData.tipoReferencia}
                    setTipo={setDataByKey}
                    setReferencia={setReferencia}
                />
                <SubmitBtn type="submit" w="fit-content" children="Entrar" />
            </Form>
        </Container>
    )
}

export default AddPergunta