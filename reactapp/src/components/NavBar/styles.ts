import styled from "styled-components";

export const NavBar = styled.nav`
    position: absolute;
    top: 90px;
    left: 25px;

    & ul {
        display: flex;
        flex-direction: column;
        gap: 5px;

        & li {
            list-style: none;
            
            &.sair, a {
                text-decoration: none;
                color: #9E9D97;
                line-height: 150%;
                font-style: normal;
                font-size: 16px;
                font-weight: 400;

                &:hover {
                    color: #858585;
                }
            }

            &.sair{
                cursor: pointer;
            }
        }
    }
`;