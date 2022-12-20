import { Dispatch, SetStateAction } from "react";

export interface IUserProvider {
    children: JSX.Element;
}

export interface IUser {
    username: string;
    email: string;
    password: string;
    whatsappNumber: number | null;
}

export type SimpleUser = Pick<IUser, "username" | "email" | "whatsappNumber">

export type AuthUser = Pick<IUser, "username" | "password">

export interface IUserProviderValue {
    authenticated?: boolean;
    user?: SimpleUser | null;
    setUser?: Dispatch<SetStateAction<SimpleUser | null>>;
    cadastrar?: (user: IUser) => void;
    login?: (user: AuthUser, callback: () => void) => void;
    logout?: () => void;
}