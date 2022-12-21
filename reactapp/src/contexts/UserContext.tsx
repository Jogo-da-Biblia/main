import React, { createContext, useEffect, useState } from "react";
import { AuthUser, IUser, IUserProvider, IUserProviderValue, SimpleUser } from "types/user";


export const UserContext = createContext<IUserProviderValue>({});

export const UserProvider: React.FC<IUserProvider> = ({ children }) => {
    // const navigate = useNavigate();
    const [user, setUser] = useState<SimpleUser | null>(null);

    useEffect(() => {
        const initApp = async () => {
            /*
            const recoveredToken = localStorage.getItem("jogo_da_biblia-token");

            if (!recoveredToken) return null

            try {
                await api.post("/token/verify/", { token: recoveredToken });
                axiosPrivate.defaults.headers.Authorization = `Bearer ${recoveredToken}`;
                const userData = await getUserData(recoveredToken);

                setUser(userData);
            } catch (err) {
                axiosPrivate.defaults.headers.Authorization = "";
            }
            */

            // temp
            // setUser(() => buscarUsuario("s"))
        };
        initApp();
    }, []);

    function buscarUsuario(token: string): SimpleUser {
        /*
        const decodedToken = jwtDecode(token);
        const user = await axiosPrivate.get(`/users/${decodedToken.user_id}/`);
        return user.data;
        */

        // temp
        const user: SimpleUser = {
            username: "admin",
            email: "admin@admin.com",
            whatsappNumber: "",
        }

        return user
    }

    async function cadastrar(userData: IUser) {
        // return api.post("/users/", userData);
    }

    function login(userData: AuthUser, callback: () => void) {
        /*
        try {
            const response = await api.post("/token/", userData);
            const { access, refresh } = response.data;

            localStorage.setItem("jogo_da_biblia-token", access);

            axiosPrivate.defaults.headers.Authorization = `Bearer ${access}`;

            const userData = await buscarUsuario(access);
            setUser({ ...userData, refreshToken: refresh, accessToken: access });
            callback();
        } catch (err) {
            return err.response;
        }
        */
    }

    function logout() {
        localStorage.removeItem("jogo_da_biblia-token")
        setUser(null)
        // axiosPrivate.defaults.headers.Authorization = null;
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