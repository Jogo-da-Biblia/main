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

export interface IUserStage extends SimpleUser{
    refreshToken?: string;
    accessToken?: string;
}
