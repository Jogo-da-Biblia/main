/* eslint-disable react-hooks/exhaustive-deps */
import React, { createContext, useEffect, useState, useContext } from "react";
import { useMutation, useManualQuery } from 'graphql-hooks'

import { IUserProvider, IUserProviderValue } from "./types"
import { ME_QUERY, VERIFY_TOKEN_MUTATION } from "./graphql_operations";

import { IUserStage } from "types/user";
import { useGrapgQLClient } from "hooks/UseGraphQLClient";


export const UserContext = createContext<IUserProviderValue>({});

export const UserProvider: React.FC<IUserProvider> = ({ children }) => {
    const [verifyTokenMutation] = useMutation(VERIFY_TOKEN_MUTATION)
    const [fetchUser] = useManualQuery(ME_QUERY)

    const client = useGrapgQLClient()
    const [user, setUser] = useState<IUserStage | null>(null);

    useEffect(() => {
        const initApp = async () => {
            const recoveredToken = localStorage.getItem("jogo_da_biblia-token");

            if (!recoveredToken) return;

            const { error } = await verifyTokenMutation({ variables: { token: recoveredToken } })

            if (error) return console.log(error)

            client.setHeader('Authorization', `JWT ${recoveredToken}`)

            const userData = await fetchUser()
            setUser(userData.data.me);

        };
        initApp();
    }, []);

    const value: IUserProviderValue = {
        authenticated: !!user,
        user,
        setUser,
        fetchUser
    }

    return <UserContext.Provider value={value} >{children}</UserContext.Provider>
}