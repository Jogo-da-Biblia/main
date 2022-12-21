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
    },
    {
        path: "adicionar-pergunta",
        element: <RouterWrapper isPrivate element={AddPergunta} />,
    },
    {
        path: "ranking",
        element: <RouterWrapper isPrivate element={Ranking} />,
    },
]);

const Routes = () => (
    <RouterProvider router={router} />
)

export default Routes;
