import styled, { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`
    :root {
        --blueColor: #537A95;
        --greyColor1: #858585;
        --greyColor2: #9E9D97;
        background-color: #F4F5F6;
    }

    body {
        
    }

    * {
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
        sans-serif;
    }

    h1, h2, h3 {
        color: #858585;
        font-family: 'Roboto Slab', serif;

    }

    p, label {
        font-family: 'Lato', sans-serif;
    }
`;

export const Label = styled.label`
    display: flex;
    margin-top: 4px;
    margin-bottom: 20px;
    flex-direction: column;
    width: auto;

    &.checkbox-container {
        position: relative;
        display: block;
        padding-left: 35px;
        margin: 15px 0;
        color: #858585;
        cursor: pointer;
        font-weight: 400;
        font-size: 16px;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        & a {
          color: #547B96;
          font-weight: 500;
        }
        input {
            position: absolute;
            height: 0;
            width: 0;
            opacity: 0;
            cursor: pointer;
        }
        &:hover input~span { background-color: #858585; }
        input:checked~span { background-color: #547B96; }
        input:checked~span:after { display: block; }
    }
`;

interface ICheckmark {
    borderRadius?: string;
    spanHidden?: boolean;
}

export const Checkmark = styled.span`
  background-color: #eee;
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  border: 1px solid #727376;
  border-radius: ${({ borderRadius }: ICheckmark) => borderRadius || "5px"};
  
  &:after {
    ${({ spanHidden }: ICheckmark) => spanHidden ? "" : "content: '';"}
    position: absolute;
    display: none;
    left: 9px;
    top: 5px;
    height: 10px;
    width: 5px;
    border: solid white;
    border-width: 0 3px 3px 0;
    transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
    -ms-transform: rotate(45deg);
}
`;