MagicBell Broadcasts allow you to send a high-level announcement to multiple users across different channels. Customizing content per channel (e.g., specific URLs for Slack vs. Email) requires using a nested `overrides` configuration, which is prone to schema errors.

You need to write a Node.js script using `fetch` or `axios` to send a POST request to `https://api.magicbell.com/v2/broadcasts` that delivers a notification to `user@example.com` with a default title and content, but specifically overrides the `action_url` for the `slack` channel.

**Constraints:**
- Ensure the API payload includes proper `X-MAGICBELL-API-KEY` and `X-MAGICBELL-API-SECRET` headers.
- The `overrides` object must strictly target the `slack` channel and provide a distinct `action_url` that differs from the default broadcast URL.