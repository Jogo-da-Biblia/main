import { Props as SelectProps } from 'react-select';

export interface IButton {
    color?: string;
    bg?: string;
    w?: string;
}

export interface ICheckmark {
    borderRadius?: string;
    spanHidden?: boolean;
}

export type MyOptionType = {
    label: string;
    value: string;
};

export type IsMulti = false;

export interface ISelectProps extends SelectProps {
    width?: string;
    error: boolean
}