import Login from "pages/Login";
import { RouterWrapper } from "./Router";
import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";

import ListaPergunta from "pages/ListaPerguntas";
import Cadastro from "pages/Cadastro";
import AddPergunta from "pages/AddPergunta";
import Ranking from "pages/Ranking";
import Home from "pages/Home";
import RedefinirSenha from "pages/RedefinirSenha";

import { listaUsuarios } from "mockData/usuarios";
import { perguntasData } from "mockData/perguntas";

import { IUserList } from "types/user";
import { IPergunta } from "global/types/pergunta";

// const ListaPergunta = lazy(() => import(""))


const fetchRankingList = () => {
    return new Promise<IUserList[]>(resolve => {
        return setTimeout(() => {
            resolve(listaUsuarios);
        }, 300);
    });
}

const fetchPerguntasList = () => {
    return new Promise<IPergunta[]>(resolve => {
        return setTimeout(() => {
            resolve(perguntasData);
        }, 300);
    });
}

const router = createBrowserRouter([
    {
        path: "/",
        element: <RouterWrapper isPrivate element={Home} />,
    },
    {
        path: "/login",
        element: <Login />,
    },
    {
        path: "cadastro",
        element: <Cadastro />,
    },
    {
        path: "/perguntas",
        element: <RouterWrapper isPrivate element={ListaPergunta} />,
        loader: async () => fetchPerguntasList()
    },
    {
        path: "adicionar-pergunta",
        element: <RouterWrapper isPrivate element={AddPergunta} />,
    },
    {
        path: "ranking",
        element: <RouterWrapper isPrivate element={Ranking} />,
        loader: async () => fetchRankingList()
    },
    {
        path: "redefinir-senha",
        element: <RouterWrapper isPrivate element={RedefinirSenha} />,
    },
]);

const Routes = () => (
    <RouterProvider router={router} />
)

export default Routes;
