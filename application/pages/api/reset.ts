import type { NextApiRequest, NextApiResponse } from 'next';
import { resetKitties } from '../../modules/persistence/kitties';

export default async function handler(
    req: NextApiRequest,
    res: NextApiResponse<unknown>
) {
    await resetKitties();

    res.status(200).end();
}
