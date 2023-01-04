import styled from "styled-components";

export const Container = styled.div`
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px;

    :where(&:nth-child(1), &:nth-child(2)) .avatar {
        border: 2px solid #FFCE5B;
    }

    & p.points {
        color: red;
    }
`;