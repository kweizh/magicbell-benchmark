# Update User Preferences via MagicBell API

## Background
You need to programmatically update a user's notification preferences for MagicBell from your Node.js backend. To do this, you must generate a User JWT and make a request to the MagicBell REST API.

## Requirements
Write a Node.js script `update_preferences.js` that performs the following:
1. Generates a User JWT for the user `user@example.com` using the `jsonwebtoken` package. The JWT payload must include `user_email` and `api_key`. It must be signed using the `HS256` algorithm.
2. Sends a `PUT` request to the MagicBell API endpoint `/channels/user_preferences` to update the user's channel preferences. Specifically, disable the `email` channel for the `updates` category.
3. The script must read the following environment variables:
   - `MAGICBELL_API_KEY`: The MagicBell API key.
   - `MAGICBELL_API_SECRET`: The MagicBell API secret (used to sign the JWT).
   - `MAGICBELL_API_URL`: The base URL for the MagicBell API (e.g., `https://api.magicbell.com/v2`).
4. The script should use the built-in `fetch` API (available in Node.js 18+) to make the request.
5. Print the HTTP status code of the response to the console.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project` and install `jsonwebtoken`.
2. Create `update_preferences.js`.
3. Use `jwt.sign` to create the token. The payload should be `{ user_email: 'user@example.com', api_key: process.env.MAGICBELL_API_KEY }`.
4. Construct the request body as JSON:
   ```json
   {
     "categories": [
       {
         "key": "updates",
         "channels": [
           { "name": "email", "enabled": false }
         ]
       }
     ]
   }
   ```
5. Send the `PUT` request to `${process.env.MAGICBELL_API_URL}/channels/user_preferences`. Remember to include the `Authorization: Bearer <token>` and `Content-Type: application/json` headers.

## Constraints
- Project path: `/home/user/project`
- Use Node.js 18+ built-in `fetch`.
- Do not hardcode the API credentials or base URL; strictly use the environment variables.

## Integrations
- None