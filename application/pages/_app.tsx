import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { PropsWithChildren, useCallback, useState } from 'react';
import { QueryClientProvider, QueryClient } from 'react-query';
import { Header } from '../components/Header';
import { AuthContext } from '../components/context/AuthContext';
import { useLocalStorage } from 'react-use';

function SafeHydrate({ children }: PropsWithChildren<unknown>) {
    return (
        <div suppressHydrationWarning>
            {typeof window === 'undefined' ? null : children}
        </div>
    );
}

function MyApp({ Component, pageProps }: AppProps) {
    const [tokenInStore, setTokenInStore, removeTokenInStore] =
        useLocalStorage<string>('token');

    const [token, setToken] = useState<string | undefined>(tokenInStore);

    const setTokenValue = (value: string | undefined) => {
        console.log('setting to ' + value);
        setTokenInStore(value);
        setToken(value);
    };

    const removeToken = () => {
        removeTokenInStore();
        setTokenValue(undefined);
    };

    const isAdmin = useCallback(() => token === 'adminToken', [token]);

    return (
        <SafeHydrate>
            <QueryClientProvider client={new QueryClient()}>
                <AuthContext.Provider
                    value={{
                        token,
                        removeToken,
                        setToken: setTokenValue,
                        isAdmin,
                    }}
                >
                    <Header />
                    <Component {...pageProps} />
                </AuthContext.Provider>
            </QueryClientProvider>
        </SafeHydrate>
    );
}

export default MyApp;
