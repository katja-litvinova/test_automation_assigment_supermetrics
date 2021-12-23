// Production-quality auth system
const adminToken = 'adminToken';
const userToken = 'userToken';

const logins = {
    'admin-adminpass': adminToken,
    'user-helloworld': userToken,
};

export const getToken = (username: string, password: string): string | null => {
    const superSecureHash = `${username}-${password}`;

    if (superSecureHash in logins) {
        return logins[superSecureHash as keyof typeof logins];
    }

    return null;
};

export const validateToken = (token: string) =>
    Object.values(logins).includes(token);
