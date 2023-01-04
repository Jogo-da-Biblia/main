import styled from "styled-components";
import { Button } from "styles/globalStyles";
// import { Label } from "styles/globalStyles";

export const Container = styled.div``;

export const Form = styled.form`
    display: flex;
    flex-direction: column;
`;

export const SubmitBtn = styled(Button)`
    align-self: flex-end;
`;

export const Select = styled.select`
    height: 55px;
    font-size: 20px;
    border: 1px solid var(--greyColor1);
    color: var(--greyColor2);
    border-radius: 5px;
    padding: 0 10px;
    outline: none;
    margin-top: 20px;
    margin-bottom: 5px;
`;

export const CheckboxLabel = styled.label`
    width: auto;
    margin: 10px 0;
    position: relative;
    display: block;
    padding-left: 35px;
    cursor: pointer;
    font-weight: 400;
    font-size: 15px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    & p {
        color: #9E9D97;
        font-size: 20px;
    }
    input {
        position: absolute;
        height: 0;
        width: 0;
        opacity: 0;
        cursor: pointer;
    }
    &:hover input~span { background-color: #ccc; }
    input:checked~span { background-color: var(--blueColor); }
    input:checked~span:after { display: block; }
`;

// export const SwitchRadio = styled.div`
//     display: flex;
//     overflow: hidden;
//     gap: 6px;
//     height: auto;
//     @media(max-width:800px) {
//         flex-wrap: wrap;
//         translate: 0;
//     }
//     @media(max-width:560px) {
//         justify-content: space-between;
//     }

//     & label {
//         margin: 0;
//     }
// `;

// export const LabelRadio = styled(Label)`
//     display: flex;
//     justify-content: center;
//     background-color: white;
//     font-size: 18px;
//     line-height: 1;
//     text-align: center;
//     padding: 0 10px;
//     transition: all 0.1s ease-in-out;
//     height: 60px;
//     border:1px solid blue;
//     border-radius: 5px;

//     &:hover {
//         cursor: pointer;
//     }
//     @media(max-width:560px) {
//         width: 90px
//     }
// `;

// export const InputRadio = styled.input`
//     position: absolute !important;
//     clip: rect(0, 0, 0, 0);
//     height: 1px;
//     width: 1px;
//     border: 0;
//     overflow: hidden;
//     &:checked + label {
//         background-color: red;
//         color: white;
//         box-shadow: none;
//     }
// `;