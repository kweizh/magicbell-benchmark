# MagicBell Webhook Event Handling

## Background
MagicBell can send webhook events when users interact with notifications. Create an Express.js server that listens for these webhooks and logs the event data.

## Requirements
- Create an Express app with a `POST /webhooks/magicbell` endpoint.
- Parse the incoming JSON payload.
- The webhook payload has the following structure: `{"event": "notification_read", "notification": {"id": "notif_123"}, "user": {"email": "test@example.com"}}`.
- If the event type is `notification_read`, append a line with the format `<notification_id> read by <user_email>` to a log file `magicbell_events.log`.
- Respond with 200 OK.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project`.
2. Install `express`.
3. Create `server.js` implementing the endpoint.

## Constraints
- Project path: `/home/user/project`
- Start command: `node server.js`
- Port: 3000
- Log file: `/home/user/project/magicbell_events.log`