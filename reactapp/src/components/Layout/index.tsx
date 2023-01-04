import Logo from "components/Logo";
import LeftBar from "components/NavBar/LeftBar";
import React from "react";
import { Container, Footer } from "./styles";

const Layout: React.FC<{ children: JSX.Element }> = ({ children }) => {
    return (
        <>
            <LeftBar />
            <Container>
                <Logo />
                {children}
                <Footer>Jogo da Bíblia 2022</Footer>
            </Container>
        </>

    );
}

export default Layout;