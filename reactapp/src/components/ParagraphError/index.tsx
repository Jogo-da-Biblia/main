import React from "react"
import { Paragraph } from "./styles"

const ParagraphError: React.FC<{ children?: string }> = ({ children }) => (
    <Paragraph>
        {children}
    </Paragraph>
)

export default ParagraphError;