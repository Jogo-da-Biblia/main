import { Dispatch, SetStateAction } from "react";

export interface IUserProvider {
    children: JSX.Element;
}

export interface IUserList {
    username: string;
    points: number;
}

export interface IUser {
    username: string;
    email: string;
    password: string;
    whatsappNumber: string;
}

export type SimpleUser = Pick<IUser, "username" | "email" | "whatsappNumber">

export type AuthUser = Pick<IUser, "username" | "password">

export interface IUserStage extends SimpleUser{
    refreshToken?: string;
    accessToken?: string;
}

export interface IUserProviderValue {
    authenticated?: boolean;
    user?: IUserStage | null;
    setUser?: Dispatch<SetStateAction<IUserStage | null>>;
    cadastrar?: (user: IUser) => void;
    login?: (user: AuthUser, callback: () => void) => void;
    logout?: () => void;
}