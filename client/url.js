const BASE_URL = 'https://test.deribit.com';
const REFRESH_TOKEN = process.env.DERIBIT_REFRESH_TOKEN; // Store your refresh token securely
let accessToken = process.env.DERIBIT_ACCESS_TOKEN; // Initial access token
let tokenExpires = Date.now() + 900000; // Set initial expiration time (e.g., 15 minutes from now)