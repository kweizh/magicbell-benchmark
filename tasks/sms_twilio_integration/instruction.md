# Configure Twilio SMS Integration for MagicBell

## Background
MagicBell supports sending SMS notifications via Twilio. You need to write a script to programmatically configure the Twilio integration for a MagicBell project using the MagicBell API.

## Requirements
- Write a bash script `setup_twilio.sh` that makes a `PUT` request to the MagicBell Twilio integration endpoint (`/v2/integrations/twilio`).
- The script must use the base URL from the `MAGICBELL_API_URL` environment variable. If `MAGICBELL_API_URL` is not set, it should default to `https://api.magicbell.com`.
- The script must authenticate using the `X-MAGICBELL-API-KEY` and `X-MAGICBELL-API-SECRET` headers, reading from the `MAGICBELL_API_KEY` and `MAGICBELL_API_SECRET` environment variables.
- The request body must be a JSON object containing the Twilio credentials:
  - `account_sid`: Read from `TWILIO_ACCOUNT_SID`
  - `api_key`: Read from `TWILIO_API_KEY`
  - `api_secret`: Read from `TWILIO_API_SECRET`
  - `from`: Read from `TWILIO_FROM_NUMBER`

## Implementation Guide
1. Create `setup_twilio.sh` in the project directory.
2. Use `curl` to send the `PUT` request. Ensure you send the `Content-Type: application/json` header.
3. Make the script executable.

## Constraints
- Project path: `/home/user/project`
- The script must handle the `MAGICBELL_API_URL` environment variable correctly without a trailing slash (e.g., `http://localhost:8080`).