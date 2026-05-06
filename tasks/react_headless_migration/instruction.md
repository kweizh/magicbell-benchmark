# Migrate MagicBell React Headless and Implement JWT Auth

## Background
Your company is updating its notification system. The frontend React app currently uses the deprecated `@magicbell/react-headless` package with an insecure client-side API key. You need to migrate it to the new unified `@magicbell/react` package and implement a secure backend to generate User JWTs.

## Requirements
1. **Backend Setup**:
   - In `/home/user/magicbell-backend`, initialize a Node.js project and install `express`, `cors`, and `jsonwebtoken`.
   - Create `server.js` that runs an Express server on port 3001.
   - Implement a `GET /auth` endpoint that generates and returns a MagicBell User JWT. The payload must contain `user_email: 'test@example.com'`. Sign it using the secret `'SUPER_SECRET_KEY'` and the `HS256` algorithm. Return it as `{ "token": "<jwt_token>" }`.
2. **Frontend Migration**:
   - In `/home/user/magicbell-migration`, uninstall `@magicbell/react-headless` and install `@magicbell/react`.
   - Update `src/App.jsx` to fetch the token from `http://localhost:3001/auth` on mount.
   - Once the token is fetched, render the MagicBell `<Provider>` (from `@magicbell/react/context-provider`) passing the token, and inside it render the `<Inbox />` component (from `@magicbell/react/inbox`). Make sure to import the CSS for the inbox (`@magicbell/react/styles/inbox.css`).

## Constraints
- Backend project path: `/home/user/magicbell-backend`
- Frontend project path: `/home/user/magicbell-migration`
- Backend port: 3001
- Frontend start command: `npm run build`
- Note: Do not change the existing React root setup in `src/main.jsx`.