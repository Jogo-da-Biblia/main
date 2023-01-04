import styled from "styled-components";

export const Container = styled.main`
    position: relative;
    background-color: white;
    min-height: 100vh;
    max-width: 500px;
    margin: auto;
    padding: 0 20px;
    padding-bottom: 50px;
`;

export const Footer = styled.footer`
    position: absolute; 
    bottom: 20px;
    left: 50%;
    translate: -50% 0;
    color: var(--greyColor2);
`;