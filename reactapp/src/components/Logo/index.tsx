import React from "react";
import logoImg from "assets/new-logo.png"
import { Container, LogoImg } from "./styles";

const Logo: React.FC<{}> = () => (
    <Container>
        <LogoImg src={logoImg} alt="" />
    </Container>

)

export default Logo;