import type { NextApiRequest, NextApiResponse } from 'next';
import { validateToken } from '../../../modules/persistence/auth';
import { readKitties } from '../../../modules/persistence/kitties';
import { Kitty } from '../../../types/Kitty';

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<Kitty[]>
) {
    const { authorization } = req.headers;
    const token = authorization?.replace('Bearer', '').trim();

    if (!authorization || !token || !validateToken(token)) {
        res.status(401).end();
    } else {
        res.status(200).json(await readKitties());
    }
}
