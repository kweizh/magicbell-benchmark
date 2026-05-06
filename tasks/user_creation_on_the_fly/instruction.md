# MagicBell User Creation On-The-Fly

## Background
MagicBell can create users on-the-fly when a notification is sent to them via a broadcast. You need to use the MagicBell REST API to trigger this behavior.

## Requirements
- Write a shell script `run.sh` that uses `curl` to send a `POST` request to the MagicBell Broadcasts API (`https://api.magicbell.com/v2/broadcasts`).
- Include the authentication headers:
  - `X-MAGICBELL-API-KEY`: `dummy_key`
  - `X-MAGICBELL-API-SECRET`: `dummy_secret`
  - `Content-Type`: `application/json`
- The JSON payload must create a broadcast with:
  - `title`: `Welcome`
  - `content`: `Hello new user`
  - `recipients`: A list containing one user with the email `new_user_on_the_fly@example.com`.
- Execute the script and save the raw HTTP response body to a log file. Since the credentials are fake, expect an error response, but you must capture it.

## Implementation Guide
1. Create `/home/user/project/run.sh` with the `curl` command.
2. Make the script executable (`chmod +x run.sh`).
3. Run the script and redirect the standard output to `/home/user/project/output.log` (e.g., `./run.sh > output.log`).

## Constraints
- Project path: `/home/user/project`
- Script file: `/home/user/project/run.sh`
- Log file: `/home/user/project/output.log`
- You must construct the correct JSON structure for the broadcast as described in the MagicBell documentation.