/** @type {import('next').NextConfig} */
module.exports = {
    target: 'serverless',
    async rewrites() {
        return [
            // Rewrite pages requests to `pages/index` (NOTE: this probably breaks dynamic pages)
            {
                source: '/pages/:any*',
                destination: '/',
            },
        ];
    },
    reactStrictMode: true,
};
