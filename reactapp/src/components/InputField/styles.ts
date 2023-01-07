import { Field } from "formik";
import styled from "styled-components";

export const Container = styled.div`
    display: flex;
    flex-direction: column;
    position: relative;

    & input {
        border: none;
        border-bottom: 1px solid whitesmoke;
        outline: none;
        transition: 300ms;
    }
    & .input-label {
        position: absolute;
        top: 30%;
        left: 20px;
        pointer-events: none;
        transition: 400ms;
        color: #9E9D97;
        font-size: 17px;
    }
`;

export const StyledField = styled(Field).attrs(props => ({
    ...props,
    style: {
        border: `1px solid ${props.bordercolor ? "red" :  '#727376'}`,
    }
}))`
    border-radius: 5px;
    padding: 20px;
    outline: none;
    font-size: 20px;
    height: 55px;
    &:hover{ background: var(--inputHoverColor); }

    &:-webkit-autofill,
    &:-webkit-autofill:hover, 
    &:-webkit-autofill:focus {
        border: 1px solid green;
    }
`;