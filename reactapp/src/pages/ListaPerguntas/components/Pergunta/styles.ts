import styled from "styled-components";

export const Container = styled.div`
    border: 1px solid #727376;
    background-color: #F4F5F6;
    border-radius: 5px;
    margin-bottom: 15px;
    padding: 10px 14px;
    
    & p {
        font-size: 14px;
        color: #9E9D97; 
        line-height: 20px;
        font-family: 'Lato', sans-serif;

        &.status {
            color: #000000;
            padding: 5px 15px;
            margin-top: 10px;
            border-radius: 15px;
            display: inline-block;
        }

        &.status-env {
            background-color: #FFCE5B;
        }
        &.status-rev {
            background-color: #5AD83A;
        }
        &.status-pub {
            background-color: blue;
        }
        &.status-neg {
            background-color: red;
        }
    }
`;