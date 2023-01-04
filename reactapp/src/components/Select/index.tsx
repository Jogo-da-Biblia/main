import { FieldProps, FormikFormProps } from "formik";
import React from "react";
import { StyledSelect } from "styles/globalStyles"

interface SelectFieldProps {
    array?: any[];
    error?: boolean;
    field?: FieldProps;
    form?: FormikFormProps;
    isDisabled?: boolean
}

const SelectField: React.FC<SelectFieldProps> = (props) => {
    let deaultOptions = [
        { value: "1", label: "primeiro" },
        { value: "2", label: "segundo" },
        { value: "3", label: "terceiro" },
    ]

    let options = props.array ?
        props.array.map(option => ({ value: option.id, label: option.name })) : deaultOptions

    return (
        <StyledSelect
            error={false}
            options={options}
            isDisabled={false}
            name={"test"}
            value={options ? options.find(option => option.value === "1") : ''}
            onChange={(option: any) => console.log(option.value)}
            onBlur={() => { }}
        />
    )
}

export default SelectField