import { useLoaderData } from "react-router-dom";
import { IUserList } from "types/user";
import UserDetail from "./components/UserDetail"
import { ListaUsuarios } from "./styles"
import { useQuery } from 'graphql-hooks'

const USERS_QUERY = `query users($limit: Int) {
    id
    username
    points
  }`

function Ranking() {
    // const { loading, error, data } = useQuery(USERS_QUERY, {
    //     variables: {
    //         limit: 10
    //     }
    // })
    let data = useLoaderData() as IUserList[];

    return (
        <>
            <h1>Ranking</h1>
            <p>Seja um colaborador pódio (7 primeiros colocados na classificação) e ganhe brindes! Veja as regras.</p>
            <ListaUsuarios>
                {
                    data.map(user => (
                        <UserDetail key={user.username} user={user} />
                    ))
                }
            </ListaUsuarios>

        </>
    )
}

export default Ranking