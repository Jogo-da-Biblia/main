import { perguntasData } from "mockData/perguntas";
import Pergunta from "./components/Pergunta";
import { Container } from "./styles";

function ListaPergunta() {
    return (
            <Container>
                <h2>Minhas Perguntas</h2>
                {
                    perguntasData.map(p => (
                        <Pergunta data={p} />
                    ))
                }
            </Container>
    )
}

export default ListaPergunta;