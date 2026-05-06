# Send a Broadcast with an Action URL

## Background
MagicBell allows you to send broadcasts to users. These broadcasts can include an `action_url` which directs the user to a specific page when they click the notification.

## Requirements
- Write a shell script `send_broadcast.sh` that sends a broadcast using the MagicBell API.
- The broadcast must have the following properties:
  - `title`: "Welcome!"
  - `content`: "Click here to get started."
  - `action_url`: "https://example.com/start"
  - `recipients`: A single recipient with the email `test@example.com`
- The script must use the `MAGICBELL_API_KEY` and `MAGICBELL_API_SECRET` environment variables for authentication.
- The script must save the raw API JSON response to `/home/user/output.json`.

## Implementation Guide
1. Create a file `/home/user/send_broadcast.sh`.
2. Write a `curl` command that sends a `POST` request to `https://api.magicbell.com/v2/broadcasts`.
3. Include the headers `X-MAGICBELL-API-KEY` and `X-MAGICBELL-API-SECRET` using the respective environment variables.
4. Set the `Content-Type: application/json` header.
5. Pass the JSON payload with the `broadcast` object containing the required fields.
6. Redirect the output of the `curl` command to `/home/user/output.json`.
7. Make the script executable (`chmod +x send_broadcast.sh`).
8. Run the script.

## Constraints
- Project path: /home/user
- Log file: /home/user/output.json
- You must use the `MAGICBELL_API_KEY` and `MAGICBELL_API_SECRET` environment variables.
