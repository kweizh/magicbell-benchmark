# MagicBell Teams Integration Script

## Background
You need to write a bash script to configure the Microsoft Teams channel integration for a user in MagicBell. This involves saving a Teams token (which contains the webhook URL) for the authenticated user via the MagicBell REST API.

## Requirements
- Write a bash script `save_teams_token.sh` that uses `curl` to save a Teams token.
- The script must accept two positional arguments:
  1. `USER_JWT`: The User JWT for authentication.
  2. `WEBHOOK_URL`: The Microsoft Teams webhook URL.
- It must send a `PUT` request to `/channels/teams/tokens`.
- The payload must be a JSON object containing the webhook URL as specified in the MagicBell documentation.
- The script must use the base URL `https://api.magicbell.com/v2` by default, but MUST allow overriding it via the `MAGICBELL_API_URL` environment variable.

## Implementation Guide
1. Create the script at `/home/user/magicbell-task/save_teams_token.sh`.
2. Ensure it has execute permissions.
3. Construct the JSON payload: `{"webhook": {"url": "<WEBHOOK_URL>"}}`.
4. Use `curl` to send the PUT request with the `Authorization: Bearer <USER_JWT>` header and `Content-Type: application/json`.

## Constraints
- Project path: `/home/user/magicbell-task`
- The script must fail (exit non-zero) if the two arguments are not provided.