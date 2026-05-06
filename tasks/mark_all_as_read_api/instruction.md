# Mark All Notifications as Read API

## Background
MagicBell provides a REST API to manage notifications. You need to write a simple shell script to mark all notifications as read for a specific user using the MagicBell API.

## Requirements
- Create a shell script at `/home/user/mark_read.sh`.
- The script must make a `POST` request to `https://api.magicbell.com/notifications/read`.
- It must include the `X-MAGICBELL-API-KEY` header, reading its value from the `MAGICBELL_API_KEY` environment variable.
- It must include the `X-MAGICBELL-USER-EMAIL` header, reading its value from the `MAGICBELL_USER_EMAIL` environment variable.
- The script must output the raw response from the API to stdout.

## Constraints
- Project path: `/home/user`