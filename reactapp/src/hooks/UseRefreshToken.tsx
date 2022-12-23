import { axiosPrivate as api } from 'api/axios';
import { IUserStage } from 'types/user';
import { useUserData } from "./UseUserData";

const useRefreshToken = () => {
    const { user, setUser } = useUserData();
    const refresh = async () => {
        if (!setUser) return;
        
        if (user?.refreshToken) {
            try {
                const response = await api.post('/token/refresh/', {
                    refresh: user.refreshToken
                });

                const newUserData: IUserStage = {...user, accessToken: response.data.access}

                setUser(newUserData);

                return response.data.access;
            } catch (err: any) {
                if (err.response.status === 401) {
                    setUser(null);
                }
            }
        } else {
            if (user) setUser(null);
            
        }
    }
    return refresh;
};
export default useRefreshToken;