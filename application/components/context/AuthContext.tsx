import { createContext } from 'react';

interface AuthContextProps {
    token?: string;
    setToken?: (token: string) => void;
    removeToken?: () => void;
    isAdmin?: () => boolean;
}

export const AuthContext = createContext<AuthContextProps>({});
