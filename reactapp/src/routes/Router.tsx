import React from "react";
import { Navigate } from "react-router-dom";
import { useUserData } from "hooks/UseUserData";
import Layout from "components/Layout";

interface IRouterWrapper {
    isPrivate?: boolean;
    element: () => JSX.Element
}

export const RouterWrapper: React.FC<IRouterWrapper> = ({ isPrivate, element: Element }) => {
    const { authenticated } = useUserData()

    if (isPrivate && !authenticated) {
        return (
            <Navigate to="/" replace />
        )
    }

    return (
        <Layout>
            <Element />
        </Layout>
    )
}