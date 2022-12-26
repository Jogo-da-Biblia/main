import React from "react";
import { StyledTextarea } from "./styles";

interface ITextArea {
    name?: string;
    id: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
}

const TextArea: React.FC<ITextArea> = ({name, id, value, onChange}) => (
    <StyledTextarea name={name} value={value} id={id} onChange={onChange} cols={30} rows={5} />
)

export default TextArea