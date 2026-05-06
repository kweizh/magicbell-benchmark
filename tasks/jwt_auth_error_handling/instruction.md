# MagicBell JWT Authentication Fix

## Background
We have a React application using the `@magicbell/react` SDK and an Express backend that provides a User JWT for authentication. However, the integration is currently failing with authentication errors, and the frontend does not handle token fetch errors gracefully.

## Requirements
1.  **Fix JWT Generation**: The Express backend (`server.js`) currently generates an invalid JWT. It must be fixed to use the correct algorithm (`HS256`) and include the required payload fields (`user_email` and `api_key`) according to MagicBell's documentation.
2.  **Frontend Error Handling**: The React frontend (`src/App.jsx`) fetches the token from `/api/token`. If the token fetch fails (e.g., backend returns 400 or 500), the app should display a visible error message `"Authentication failed"` in a `div` with `id="error-message"`.

## Implementation Guide
1.  Update `server.js`: Fix the `jwt.sign` call. Ensure it uses the `MAGICBELL_API_SECRET` to sign an `HS256` token containing `user_email` and `api_key` (using `MAGICBELL_API_KEY`).
2.  Update `src/App.jsx`: Ensure that if the token fetch fails, the UI displays `<div id="error-message">Authentication failed</div>`. Do not render the MagicBellProvider if there is an error or no token.

## Constraints
- Project path: `/home/user/magicbell-app`
- Start command: `npm run dev` (starts both frontend and backend concurrently)
- Frontend Port: 3000
- Backend Port: 3001

## Integrations
- None