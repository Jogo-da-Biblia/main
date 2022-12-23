import { useUserData } from "hooks/UseUserData"
import React from "react"
import { NavLink } from "react-router-dom"
import navData from "./data"
import { NavBar } from "./styles"

const LeftBar: React.FC<{}> = () => {
    const { logout } = useUserData()

    const activeStyle = {
        color: "#858585"
    }

    return (
        <NavBar>
            <ul>
                {
                    navData.map((link, index) => (
                        <li key={index}>
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