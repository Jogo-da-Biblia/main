import { useGrapgQLClient } from "hooks/UseGraphQLClient"
import { useUserData } from "hooks/UseUserData"
import React from "react"
import { NavLink } from "react-router-dom"
import navData from "./data"
import { NavBar } from "./styles"

const LeftBar: React.FC<{}> = () => {
    const { setUser } = useUserData()
    const client = useGrapgQLClient()

    const logout = () => {
        localStorage.removeItem("jogo_da_biblia-token")
        setUser(null)
        client.setHeader('Authorization', null)
    }

    const activeStyle = {
        color: "#858585"
    }

    return (
        <NavBar>
            <ul>
                {
                    navData.map((link, i) => (
                        <li key={i}>
                            <NavLink
                                to={link.to || "../"}
                                style={({ isActive }) =>
                                    isActive ? activeStyle : undefined
                                }
                            >{link.label}</NavLink>
                        </li>
                    ))
                }
                <li className="sair" onClick={logout}>Sair</li>
            </ul>
        </NavBar>
    )
}

export default LeftBar