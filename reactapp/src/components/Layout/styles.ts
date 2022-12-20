import styled from "styled-components";

export const NavBar = styled.nav`
    position: absolute;
    top: 90px;
    left: 25px;

    & ul {
        display: flex;
        flex-direction: column;
        gap: 7px;

        & li {
            list-style: none;
            & a {
                text-decoration: none;
                color: #9E9D97;

                &:hover {
                    color: #858585;
                }
            }
        }
    }
`;