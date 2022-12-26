import Logo from "components/Logo";
import LeftBar from "components/NavBar/LeftBar";
import React from "react";
import { Container } from "./styles";

const Layout: React.FC<{ children: JSX.Element }> = ({ children }) => {
    return (
        <Container>
            <LeftBar />
            <Logo />
            {children}
        </Container>
    );
}

export default Layout;