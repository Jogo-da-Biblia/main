/* eslint-disable react-hooks/exhaustive-deps */
import React from 'react'
import { GraphQLClient, ClientContext } from 'graphql-hooks'
// import { buildAxiosFetch } from '@lifeomic/axios-fetch'

export const BASE_URL = process.env.REACT_APP_API || "http://localhost:8001/api/v1"

const client = new GraphQLClient({
    url: `${BASE_URL}/graphql/`,
    // fetch: buildAxiosFetch(useAxios)
})

interface IGraphQLClientProps {
    children: JSX.Element
}

const GraphQLClientProvider: React.FC<IGraphQLClientProps> = ({ children }) => {
    return (
        <ClientContext.Provider value={client} >
            {children}
        </ClientContext.Provider>
    )
}

export default GraphQLClientProvider