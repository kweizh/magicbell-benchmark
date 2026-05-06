# MagicBell Multi-Channel Broadcast Payload

## Background
You need to construct a MagicBell broadcast payload for a multi-channel delivery system. The broadcast should alert an admin and provide a default action URL, but use a specific action URL when delivered via Slack.

## Requirements
1. Initialize a Node.js project in `/home/user/magicbell-project`.
2. Write a Node.js script `build_payload.js` that generates a valid JSON payload for the MagicBell Create Broadcast API (`POST /broadcasts`).
3. The generated JSON must have a top-level `broadcast` object containing:
   - `title`: 'Alert'
   - `content`: 'System down'
   - `action_url`: 'https://example.com/alert'
   - `recipients`: An array with one object `{"email": "admin@example.com"}`
   - `overrides`: An object configuring the `slack` channel to use `action_url`: 'https://example.com/slack-alert' (nested under `channels.slack`).
4. Run the script and write the JSON output to `payload.json`.

## Implementation Guide
1. `mkdir -p /home/user/magicbell-project` and `cd` into it.
2. `npm init -y`
3. Create `build_payload.js` that constructs the JavaScript object and uses `fs.writeFileSync('payload.json', JSON.stringify(payload, null, 2))`.
4. Run `node build_payload.js`.

## Constraints
- Project path: `/home/user/magicbell-project`
- Log file: `/home/user/magicbell-project/payload.json`