# MagicBell Custom Email Template Broadcast

## Background
MagicBell allows sending cross-channel notifications. You need to write a Node.js script that sends a broadcast notification with a custom HTML template specifically for the email channel using the MagicBell REST API.

## Requirements
- Initialize a Node.js project in `/home/user/magicbell-project`.
- Install `axios`.
- Create a script `/home/user/magicbell-project/send_broadcast.js`.
- The script must make a POST request to `https://api.magicbell.com/v2/broadcasts` using `axios`.
- It must use the headers `X-MAGICBELL-API-KEY: dummy_key` and `X-MAGICBELL-API-SECRET: dummy_secret`.
- The broadcast payload must include:
  - `title`: "Welcome to our platform"
  - `recipients`: An array with one recipient `{"email": "newuser@example.com"}`
  - `overrides`: A channel override for `email` containing `html`: "<h1>Welcome!</h1><p>Thanks for joining.</p>" and `title`: "Welcome Email".

## Implementation Guide
1. `cd /home/user/magicbell-project`
2. `npm init -y`
3. `npm install axios`
4. Write `send_broadcast.js` to send the request and `console.log` the response.

## Constraints
- Project path: `/home/user/magicbell-project`
- The script must be executable via `node send_broadcast.js`.
- Use `axios` for the HTTP request.