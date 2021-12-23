import type { NextApiRequest, NextApiResponse } from 'next';
import { getToken } from '../../modules/persistence/auth';

interface Success {
    token: string;
}

interface Error {
    error: string;
}

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<Success | Error>
) {
    const { username, password } = req.body;

    if (
        !username ||
        !password ||
        typeof username !== 'string' ||
        typeof password !== 'string'
    ) {
        res.status(400).json({ error: 'Missing username or password' });
    } else {
        const token = getToken(username, password);

        if (token) {
            res.status(200).json({
                token,
            });
        } else {
            res.status(401).json({ error: 'Incorrect username or password' });
        }
    }
}
