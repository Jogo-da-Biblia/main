import { useContext } from "react";
import { ClientContext } from 'graphql-hooks'


export const useGrapgQLClient = () => useContext(ClientContext)