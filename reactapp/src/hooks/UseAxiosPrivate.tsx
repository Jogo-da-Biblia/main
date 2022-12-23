/* eslint-disable react-hooks/exhaustive-deps */
import { axiosPrivate } from "api/axios";
import { useEffect } from "react";
import useRefreshToken from "./UseRefreshToken";
import { useUserData } from "./UseUserData";

const useAxiosPrivate = () => {
    const refresh = useRefreshToken();
    const { user } = useUserData();

    useEffect(() => {

        const requestIntercept = axiosPrivate.interceptors.request.use(
            config => {
                config.headers!.Authorization = `Bearer ${user?.accessToken}`;
                return config;
            }, (error) => Promise.reject(error)
        );

        const responseIntercept = axiosPrivate.interceptors.response.use(
            response => response,
            async (error) => {
                const prevRequest = error?.config;
                if (error?.response?.status === 401 && !prevRequest?.sent) {
                    prevRequest.sent = true;
                    //console.log(user.refreshToken)
                    const newAccessToken = await refresh();
                    prevRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                    return axiosPrivate(prevRequest);
                }
                return Promise.reject(error);
            }
        );

        return () => {
            axiosPrivate.interceptors.request.eject(requestIntercept);
            axiosPrivate.interceptors.response.eject(responseIntercept);
        }
    }, [])

    return axiosPrivate;
}

export default useAxiosPrivate;