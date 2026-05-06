# MagicBell Transactional Notification via Stripe Webhook

## Background
MagicBell is a notification-as-a-service platform. In this task, you will integrate MagicBell with a Stripe webhook to send a transactional notification when a user's payment succeeds.

## Requirements
- Create an Express.js server that listens on port 3000.
- Implement a `POST /webhook/stripe` endpoint.
- When the endpoint receives a Stripe webhook event with `type: "invoice.payment_succeeded"`, it must send a MagicBell Broadcast.
- The MagicBell Broadcast payload must be:
  ```json
  {
    "broadcast": {
      "title": "Payment Successful",
      "content": "Your payment for subscription <subscription_id> was successful.",
      "recipients": [{ "email": "<customer_email>" }]
    }
  }
  ```
- The `<subscription_id>` and `<customer_email>` must be extracted from the Stripe event payload (`req.body.data.object.subscription` and `req.body.data.object.customer_email`).
- The MagicBell API request must be sent to the URL specified by the `MAGICBELL_API_URL` environment variable (default to `https://api.magicbell.com` if not set).
- The MagicBell API request must include the `X-MAGICBELL-API-KEY` and `X-MAGICBELL-API-SECRET` headers, sourced from the `MAGICBELL_API_KEY` and `MAGICBELL_API_SECRET` environment variables.
- Return a 200 OK response to the Stripe webhook after processing.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/magicbell-stripe`.
2. Install `express` (and any HTTP client like `axios` if you prefer, or use built-in `fetch`).
3. Create `index.js` and implement the Express server with the `/webhook/stripe` endpoint. Make sure to use `express.json()` middleware to parse the request body.
4. Ensure the server listens on port 3000.

## Constraints
- Project path: `/home/user/magicbell-stripe`
- Start command: `node index.js`
- Port: 3000
- You must use the `MAGICBELL_API_URL`, `MAGICBELL_API_KEY`, and `MAGICBELL_API_SECRET` environment variables.