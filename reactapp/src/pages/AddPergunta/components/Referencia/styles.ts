import styled from "styled-components";

export const Container = styled.div`
    & p.op1-inf {
        color: var(--greyColor2);
        font-size: 12px;
        font-style: italic;
        line-height: 14px;
        margin-left: 40px;
    }
`;


export const SelectContainer = styled.div`
    display: flex;
    flex-direction: column;
    /* gap: 15px; */
    margin: 20px 0;
    
    & select {
        margin: 0;
    }
`;