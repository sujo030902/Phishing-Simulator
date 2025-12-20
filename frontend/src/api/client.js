import axios from 'axios';

const api = axios.create({
    // Vercel handles /api routing automatically to the backend functions
    // In local development with 'vercel dev', this also works.
    baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;
