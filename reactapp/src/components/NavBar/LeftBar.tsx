import React from "react"
import { NavLink } from "react-router-dom"
import navData from "./data"
import { NavBar } from "./styles"

const LeftBar: React.FC<{}> = () => {

    const activeStyle = {
        color: "#858585"
    }

    return (
        <NavBar>
            <ul>
                {
                    navData.map(link => (
                        <li>
                            <NavLink
                                to={link.to || "../"}
                                style={({ isActive }) =>
                                    isActive ? activeStyle : undefined
                                }
                            >{link.label}</NavLink>
                        </li>
                    ))
                }
            </ul>
        </NavBar>
    )
}

export default LeftBar