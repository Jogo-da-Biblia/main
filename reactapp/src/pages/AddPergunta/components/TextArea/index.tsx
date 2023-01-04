import React from "react";
import { StyledTextarea } from "./styles";

interface ITextArea {
    name?: string;
    placeholder?: string;
    id: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
}

const TextArea: React.FC<ITextArea> = props => (
    <StyledTextarea
        {...props}
        onChange={props.onChange}
        cols={30}
        rows={5}
    />
)

export default TextArea