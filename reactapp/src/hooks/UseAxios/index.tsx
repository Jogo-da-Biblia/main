/* eslint-disable react-hooks/exhaustive-deps */
import { useEffect } from "react";
import { useMutation } from 'graphql-hooks'
import axios from "axios"

import { IUserStage } from "types/user";
import { REFRESH_TOKEN_MUTATION } from "./graphql_operations";
import { useUserData } from "hooks/UseUserData";
import { useGrapgQLClient } from "hooks/UseGraphQLClient";

const api = axios.create();


const useAxios = () => {
    const { user, setUser } = useUserData();
    const [refreshToken] = useMutation(REFRESH_TOKEN_MUTATION)
    const client = useGrapgQLClient()

    useEffect(() => {
        const responseIntercept = api.interceptors.response.use(
            (res: any) => res,
            async (error: any) => {
                const prevRequest = error?.config;
                if (error?.response?.status === 401 && !prevRequest?.sent) {
                    prevRequest.sent = true;

                    if (!setUser) return;

                    if (user?.token) {
                        const { data, error } = await refreshToken({ variables: { token: user.token } })

                        if (error) return setUser(null);

                        let token = data.refreshToken

                        const newUserData: IUserStage = { ...user, token }

                        setUser(newUserData);

                        localStorage.setItem("jogo_da_biblia-token", token);
                        client.setHeader('Authorization', `JWT ${token}`)

                    } else {
                        if (user) setUser(null);
                    }

                    return api(prevRequest);
                }
                return Promise.reject(error);
            }
        );

        return () => {
            api.interceptors.response.eject(responseIntercept);
        }
    }, [])

    return api;
}

export default useAxios;