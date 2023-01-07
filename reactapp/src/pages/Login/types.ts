import { IUser } from "global/types/user";


export type AuthUser = Pick<IUser, "username" | "password">