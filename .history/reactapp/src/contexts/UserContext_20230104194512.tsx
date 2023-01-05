import { api, axiosPrivate } from "api/axios";
import jwtDecode from "jwt-decode";
import React, { createContext, useEffect, useState } from "react";
import { AuthUser, IUser, IUserProvider, IUserProviderValue, IUserStage } from "types/user";


export const UserContext = createContext<IUserProviderValue>({});

export const UserProvider: React.FC<IUserProvider> = ({ children }) => {
    // const navigate = useNavigate();
    const [user, setUser] = useState<IUserStage | null>(null);

    useEffect(() => {
        const initApp = async () => {
            const recoveredToken = localStorage.getItem("jogo_da_biblia-token");

            console.log()

            if (!recoveredToken) return;

            try {
                await api.post("/token/verify/", { token: recoveredToken });
                axiosPrivate.defaults.headers.Authorization = `Bearer ${recoveredToken}`;
                const userData = await buscarUsuario(recoveredToken);

                setUser(userData);
            } catch (err) {
                axiosPrivate.defaults.headers.Authorization = "";
            }

            // temp
            // setUser(() => buscarUsuario("s"))
        };
        initApp();
    }, []);

    async function buscarUsuario(token: string): Promise<IUserStage> {
        const decodedToken = jwtDecode(token);
        const res = await axiosPrivate.post(`/graphql/`, {
            query: `{
                    user (id:${decodedToken.user_id}) {
                        username
                        email
                        name
                        phone
                    }
                }`
        });
        const { usuario } = res.data.data
        return usuario;

        // temp
        // const user: IUserStage = {
        //     username: "admin",
        //     email: "admin@admin.com",
        //     whatsappNumber: "",
        // }

        // return user
    }

    async function cadastrar(userData: IUser) {
        // return api.post("/users/", userData);
    }

    async function login(data: AuthUser, callback: () => void | any) {
        try {
            const response: any = await api.post("/token/", data);
            const { access, refresh } = response.data;

            localStorage.setItem("jogo_da_biblia-token", access);

            axiosPrivate.defaults.headers.Authorization = `Bearer ${access}`;

            const userData = await buscarUsuario(access);
            setUser({ ...userData, refreshToken: refresh, accessToken: access });
            callback();
        } catch (err: any) {
            return err.response;
        }
    }

    function logout() {
        localStorage.removeItem("jogo_da_biblia-token")
        setUser(null)
        axiosPrivate.defaults.headers.Authorization = null;
    }

    const value: IUserProviderValue = {
        authenticated: !!user,
        user,
        cadastrar,
        login,
        logout,
        setUser
    }

    return <UserContext.Provider value={value} >{children}</UserContext.Provider>
}