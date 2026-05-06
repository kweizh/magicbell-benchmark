# Fetch Notifications using MagicBell API

## Background
You need to write a shell script that fetches the list of notifications for a specific user via the MagicBell REST API.

## Requirements
- Create a shell script named `fetch_notifications.sh` in the project directory.
- The script must contain a single `curl` command to fetch all notifications for a user.
- The endpoint to use is `https://api.magicbell.com/v2/notifications`.
- You must authenticate using the provided User JWT: `dummy_user_jwt_token`.
- Pass the JWT in the `Authorization` header as a Bearer token.
- The script should output the JSON response to standard output.

## Constraints
- Project path: `/home/user/project`
- Script file: `/home/user/project/fetch_notifications.sh`
- The script must be executable.

## Integrations
- None