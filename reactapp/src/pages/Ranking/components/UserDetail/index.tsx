import React from "react"
import { IUserList } from "types/user"
import { Container } from "./styles"
import { Avatar } from "@mui/material"

interface IUserDetail {
    user: IUserList
}

const UserDetail: React.FC<IUserDetail> = ({ user }) => {
    return (
        <Container>
            <Avatar className="avatar" src="/broken-image.jpg" />
            <p className="username">{user.username}</p>
            <p className="points">{user.points} pts</p>
        </Container>
    )
}


export default UserDetail