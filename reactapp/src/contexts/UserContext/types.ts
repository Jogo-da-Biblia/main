import { Dispatch, SetStateAction } from "react";

import { IUserStage } from "global/types/user";


export interface IUserProvider {
    children: JSX.Element;
}

export interface IUserProviderValue {
    authenticated?: boolean;
    user?: IUserStage | null;
    setUser?: Dispatch<SetStateAction<IUserStage | null>>;
    fetchUser?: () => any;
}