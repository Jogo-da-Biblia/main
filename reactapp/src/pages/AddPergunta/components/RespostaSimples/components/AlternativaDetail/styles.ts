import styled from "styled-components";

export const Container = styled.div`
    border: 1px solid var(--greyColor1);
    border-radius: 5px;
    margin: 5px 0;
    padding: 10px;
    font-size: 20px;
    color: var(--greyColor2);
`;

export const AlternativaLabel = styled.p`
    ${({correta} : {correta: boolean}) => correta ? "color: var(--blueColor) !important;" : ""}
`;

export const Controls = styled.div`
    display: flex;
    justify-content: space-between;
`;

export const DeleteBtn = styled.button`
    border: none;
    background-color: transparent;
    cursor: pointer;
`;