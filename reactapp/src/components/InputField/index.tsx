import React from "react";
import { Container, StyledField } from "./styles";

interface IInputField {
    label?: string;
    bordercolor: "" | boolean | undefined;
    value: string | null;
    [rest: string]: any;
}

const InputField = ({ label, bordercolor, value, ...rest }: IInputField) => {
    const labelRef = React.useRef<HTMLLabelElement | null>(null);
    const inputRef = React.useRef<HTMLInputElement | null>(null);

    const focusIn = () => {
        if (labelRef.current) {
            labelRef.current.style.top = "0";
            labelRef.current.style.fontSize = "0.9rem";
        }
    }

    const focusOut = () => {
        if (labelRef.current && !(value)) {
            labelRef.current.style.top = "30%";
            labelRef.current.style.left = "20px";
            labelRef.current.style.fontSize = "17px";
        }
    }

    return (
        <Container>
            <label ref={labelRef} className="input-label">{label || "label ?"}</label>
            <StyledField
                ref={inputRef}
                bordercolor={bordercolor}
                onFocus={focusIn}
                onBlur={focusOut}
                {...rest} />
        </Container>
    )
}

export default InputField