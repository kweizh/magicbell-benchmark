# Delete Notification via MagicBell API

## Background
You need to delete a specific notification using the MagicBell REST API.

## Requirements
- Use `curl` to send a DELETE request to the MagicBell API to delete a notification with ID `notif_123`.
- The API Key is `dummy_api_key` and API Secret is `dummy_api_secret`.
- Extract the HTTP status code from the response and save it to `/home/user/output.txt`.

## Implementation Guide
1. Send a DELETE request to `https://api.magicbell.com/notifications/notif_123` using `curl`.
2. Include the headers `X-MAGICBELL-API-KEY: dummy_api_key` and `X-MAGICBELL-API-SECRET: dummy_api_secret`.
3. Extract the HTTP status code (e.g., using `-w "%{http_code}"`) and write it to `/home/user/output.txt`.

## Constraints
- Project path: /home/user
- Log file: /home/user/output.txt
- You must use `curl`.