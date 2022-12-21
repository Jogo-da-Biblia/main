import styled from "styled-components";
import { Field } from "formik"


export const Container = styled.div`
    background-color: white;
    min-height: 100vh;
    width: 500px;
    margin: auto;
    padding-bottom: 40px;

    & form {
        padding: 20px;
        & p {
           margin: 20px 0; 
        }
    }

    & .logo {
        width: 100%;
        height: 250px;
        object-fit: cover;
    }
`;

export const InputsContainer = styled.div`
    display: flex;
    flex-direction: column;
    gap: 10px;
`;

export const SubmitBtn = styled.button`
    float: right;
    margin: 10px 0;
    font-size: 20px;
    background-color: #547B96;
    color: white;
    border: none;
    padding: 10px 25px;
    border-radius: 5px;
`;