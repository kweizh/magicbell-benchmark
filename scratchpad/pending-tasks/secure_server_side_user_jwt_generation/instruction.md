To securely authenticate a frontend user with MagicBell, developers must generate a User JWT on the server side to prevent exposing the API Secret. A common friction point is using the wrong signing algorithm or missing required payload fields, which leads to `401 Unauthorized` errors.

You need to create a Node.js Express endpoint (`GET /api/auth/magicbell`) that generates and returns a signed User JWT for a requested `user_email` query parameter. 

**Constraints:**
- The JWT payload MUST contain exactly `user_email` and `api_key`.
- You MUST sign the token using the `HS256` algorithm (do NOT use `RS256`).
- The endpoint must return the token as a JSON response: `{ "token": "<GENERATED_JWT>" }`.