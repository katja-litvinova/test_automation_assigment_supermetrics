import axios from 'axios';
import { useRouter } from 'next/router';
import { ComponentType, useCallback, useContext } from 'react';
import styled from 'styled-components';
import { AuthContext } from './context/AuthContext';

const Nav = styled.nav`
    position: sticky;
    z-index: 1;
    top: 0;
    width: 100%;
    background-color: #d32329;
    padding: 10px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
`;

const HeaderText = styled.span`
    font-size: 26pt;
    color: #fbe2d6;
`;

const Button = styled.button`
    background-color: #3d3d3d;
    color: #fbe2d6;
    font-size: 16pt;
`;

export const Header: ComponentType<unknown> = () => {
    const { token, removeToken } = useContext(AuthContext);

    const isLoggedIn = !!token;

    const onLogInOutClick = useCallback(() => {
        if (isLoggedIn) {
            removeToken?.();
        } else {
            router.push('/login');
        }
    }, [isLoggedIn]);

    const router = useRouter();

    return (
        <Nav>
            <HeaderText>Supermetrics Kitty Manager</HeaderText>
            <div>
                <Button
                    onClick={() => {
                        axios
                            .post(
                                `http://${process.env.NEXT_PUBLIC_API_URL}/api/reset`
                            )
                            .then(() => window.location.reload());
                    }}
                >
                    Reset
                </Button>
                <Button onClick={onLogInOutClick}>
                    {isLoggedIn ? 'Log out' : 'Log in'}
                </Button>
            </div>
        </Nav>
    );
};
