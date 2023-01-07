import { useContext } from "react";
import { UserContext } from "contexts/UserContext";


export const useUserData = () => useContext(UserContext)