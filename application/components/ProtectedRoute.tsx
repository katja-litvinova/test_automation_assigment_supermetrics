import { useRouter } from 'next/router';
import React, { ComponentType, PropsWithChildren, useContext } from 'react';
import { AuthContext } from './context/AuthContext';

export const ProtectedRoute =
    <P extends PropsWithChildren<object>>(
        ProtectedComponent: ComponentType<P>
    ) =>
    (props: P) => {
        const { token } = useContext(AuthContext);
        const router = useRouter();

        if (!token) {
            router.push('/login');
        }

        return (
            <ProtectedComponent {...props}>{props.children}</ProtectedComponent>
        );
    };
