import { perguntasData } from "mockData/perguntas";
import Pergunta from "./components/Pergunta";
import { Container, Content } from "./styles";

function ListaPergunta() {
    return (
        <Container>
            <Content>
                <h2>Minhas Perguntas</h2>
                {
                    perguntasData.map(p => (
                        <Pergunta data={p} />
                    ))
                }
            </Content>
        </Container>
    )
}

export default ListaPergunta;