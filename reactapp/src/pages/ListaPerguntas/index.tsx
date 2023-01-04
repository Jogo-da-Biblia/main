import { useLoaderData } from "react-router-dom";
import { IPergunta } from "types/pergunta";
import Pergunta from "./components/Pergunta";
import { Container } from "./styles";
import { useQuery } from 'graphql-hooks'

const PERGUNTAS_QUERY = `query perguntas($limit: Int) {
    id
    enumciado
    resposta
    tipoResposta
    status
  }`

function ListaPergunta() {
    // const { loading, error, data } = useQuery(PERGUNTAS_QUERY, {
    //     variables: {
    //         limit: 10
    //     }
    // })
    let data = useLoaderData() as IPergunta[];

    return (
            <Container>
                <h2>Minhas Perguntas</h2>
                {
                    data.map((p, index) => (
                        <Pergunta key={index} data={p} />
                    ))
                }
            </Container>
    )
}

export default ListaPergunta;