import LeftBar from "components/NavBar/LeftBar";
import React from "react";
import { Container } from "./styles";

const Layout: React.FC<{ children: JSX.Element }> = ({ children }) => {
    return (
        <Container>
            <LeftBar />
            {children}
        </Container>
    );
}

export default Layout;