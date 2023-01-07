import { FieldProps, FormikFormProps } from "formik";
import React, { useState, useLayoutEffect } from "react";
import { StyledSelect } from "global/styles/globalStyles"

interface SelectFieldProps {
    array?: any[];
    optionValue: string;
    optionLabel: string;
    setValue: () => void;
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
        props.array.map(option => ({
            value: option[props.optionValue], label: option[props.optionLabel]
        })) : deaultOptions

    return (
        <StyledSelect
            placeholder={options.find((option: any) => option.value === String(props.value)).label}
            error={false}
            options={options}
            isDisabled={false}
            name={"test"}
            value={options ? options.find(option => option.value === props.value) : ''}
            onChange={(option: any) => props.setValue(option.value)}
            onBlur={() => { }}
        />
    )
}

export default SelectField