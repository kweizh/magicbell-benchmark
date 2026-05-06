# Fetch Notifications with Pagination

## Background
MagicBell provides a REST API to fetch a user's notifications. You need to write a script that fetches all notifications for a given user using the `GET /notifications` endpoint, handling pagination to ensure all records are retrieved.

## Requirements
- Write a Node.js script `fetch_notifications.js` in `/home/user/magicbell-task`.
- The script must generate a User JWT for `test_user@example.com` using the `jsonwebtoken` package with the `HS256` algorithm. The JWT payload must include `user_email` and `api_key`.
- Use the generated JWT to authenticate with the MagicBell API.
- Fetch all notifications for the user by making requests to `<MAGICBELL_API_URL>/notifications`.
- Implement pagination using the `limit` (e.g., set to 2) and `starting_after` query parameters until no more notifications are returned.
- Extract the `title` of each notification and save the full list of titles as a JSON array to `/home/user/magicbell-task/output.json`.

## Implementation Guide
1. Initialize a Node.js project and install `jsonwebtoken` and `axios` (or use built-in `fetch`).
2. Read `MAGICBELL_API_KEY`, `MAGICBELL_API_SECRET`, and `MAGICBELL_API_URL` from environment variables. If `MAGICBELL_API_URL` is not set, default to `https://api.magicbell.com/v2`.
3. Generate the User JWT using the secret.
4. Make a `GET` request to `${MAGICBELL_API_URL}/notifications?limit=2` with the `Authorization: Bearer <JWT>` header or `X-MAGICBELL-USER-JWT: <JWT>`.
5. The response contains a `notifications` array. If it's not empty, get the `id` of the last notification and use it as `starting_after` in the next request.
6. Keep fetching until the `notifications` array is empty.
7. Write the collected titles to `output.json`.

## Constraints
- Project path: `/home/user/magicbell-task`
- Log file: `/home/user/magicbell-task/output.json`
- Run command: `node fetch_notifications.js`
- Environment variables: `MAGICBELL_API_KEY`, `MAGICBELL_API_SECRET`, `MAGICBELL_API_URL`