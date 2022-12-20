import React from "react";
import { NavBar } from "./styles";

const Layout: React.FC<{ children: JSX.Element }> = ({ children }) => {
    return (
        <>
            <NavBar >
                <ul>
                    <li>
                        <a href="/">Adicionar Pergunta</a>
                    </li>
                    <li>
                        <a href="/">Minhas Perguntas</a>
                    </li>
                    <li>
                        <a href="/">Ranking</a>
                    </li>
                    <li>
                        <a href="/">Redefinir Senha</a>
                    </li>
                    <li>
                        <a href="/">Sair</a>
                    </li>
                </ul>
            </NavBar>
            {children}
        </>
    );
}

export default Layout;