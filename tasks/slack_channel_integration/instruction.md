# MagicBell Slack Integration

## Background
MagicBell supports multi-channel notifications, including Slack. You need to write a script to send a broadcast specifically formatted for Slack using channel overrides.

## Requirements
- Write a bash script `send_slack_broadcast.sh` that uses `curl` to call the MagicBell `POST /broadcasts` endpoint.
- The broadcast should have a general title "System Alert" and content "General alert message".
- It must include an override for the `slack` channel with the content "Slack-specific alert message".
- The recipient should be `user@example.com`.
- Use the API key and secret passed as environment variables `MAGICBELL_API_KEY` and `MAGICBELL_API_SECRET`.

## Implementation Guide
1. Create `/home/user/myproject/send_slack_broadcast.sh`.
2. Ensure the script is executable.
3. Use `curl` to send a POST request to `https://api.magicbell.com/v2/broadcasts`.
4. Set the `X-MAGICBELL-API-KEY` and `X-MAGICBELL-API-SECRET` headers.
5. The JSON payload must include:
   - `broadcast.title`: "System Alert"
   - `broadcast.content`: "General alert message"
   - `broadcast.recipients`: `[{"email": "user@example.com"}]`
   - `broadcast.overrides.slack.content`: "Slack-specific alert message"
6. Output the HTTP response body to stdout.

## Constraints
- Project path: /home/user/myproject
- Script path: /home/user/myproject/send_slack_broadcast.sh
- The script must read `MAGICBELL_API_KEY` and `MAGICBELL_API_SECRET` from the environment.