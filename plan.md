# Evaluation Dataset Research: MagicBell
MagicBell is a "Notification-as-a-Service" platform that provides a complete notification infrastructure, including a pre-built embeddable inbox, cross-channel delivery (Email, Push, Slack, SMS), and preference management. It is designed to replace custom-built notification systems with a scalable, multi-channel solution.
## 1. Library Overview
*   **Description**: A full-stack notification platform that provides an embeddable UI (Inbox) and a backend API to manage and deliver notifications across multiple channels.
*   **Ecosystem Role**: Acts as the notification layer in a tech stack, sitting between the application logic (which triggers notifications) and the delivery providers (SendGrid, Twilio, APNs, etc.).
*   **Project Setup**:
    1.  Create a project in the [MagicBell Dashboard](https://app.magicbell.com/).
    2.  Obtain the **API Key** and **API Secret** from the Settings > User Auth page.
    3.  Install the React SDK: `npm install @magicbell/react`.
    4.  Initialize the provider in your React app with a **User JWT** generated on your server.
## 2. Core Primitives & APIs
### Primitives
*   **Broadcast**: A high-level announcement sent to one or many users. Creating a broadcast generates individual notifications.
*   **Notification**: An individual instance of a message for a specific user, tracking state (read, seen, archived).
*   **User**: Identified by `email` or `external_id`. MagicBell can create users on-the-fly when a notification is sent or when they log into the inbox.
*   **Channel**: Mediums like `in_app`, `email`, `mobile_push`, `web_push`, `slack`, `sms`, `teams`.
### Key APIs
*   **Create Broadcast (`POST /broadcasts`)**:
    ```bash
    curl https://api.magicbell.com/v2/broadcasts \
      -X POST \
      -H "X-MAGICBELL-API-KEY: <API_KEY>" \
      -H "X-MAGICBELL-API-SECRET: <API_SECRET>" \
      -d '{
        "broadcast": {
          "title": "New Comment",
          "content": "You have a new comment on your post",
          "recipients": [{ "email": "user@example.com" }]
        }
      }'
    ```
    *Documentation: [Create Broadcast](https://www.magicbell.com/docs/api/reference#create_broadcast)*
*   **User JWT Generation (Server-side)**:
    ```typescript
    import jwt from 'jsonwebtoken';
    const token = jwt.sign({
      user_email: 'user@example.com',
      api_key: 'YOUR_API_KEY'
    }, 'YOUR_API_SECRET', { algorithm: 'HS256' });
    ```
    *Documentation: [User JWT](https://www.magicbell.com/docs/api/authentication/user)*
*   **React Components**:
    ```jsx
    import MagicBellProvider from '@magicbell/react/context-provider';
    import FloatingInbox from '@magicbell/react/floating-inbox';
    <MagicBellProvider token={userJwt}>
      <FloatingInbox />
    </MagicBellProvider>
    ```
    *Documentation: [React Components](https://www.magicbell.com/docs/libraries/magicbell-react)*
## 3. Real-World Use Cases & Templates
*   **SaaS Activity Feeds**: Using the `FloatingInbox` to show real-time updates (mentions, comments, task assignments).
*   **Multi-Channel Alerts**: Sending a single notification that triggers an In-App message and an Email fallback if not seen within X minutes (configured via Delivery Planner).
*   **User Preference Centers**: Using the `UserPreferences` component to allow users to opt-out of specific categories or channels.
*   **Transactional Notifications**: Integrating with Stripe to notify users of successful payments or subscription failures.
## 4. Developer Friction Points
*   **JWT Signing Errors**: Developers often use the wrong algorithm (e.g., RS256 instead of HS256) or include incorrect payload fields, leading to `401 Unauthorized` errors. [Discussion](https://github.com/orgs/magicbell/discussions/254)
*   **Service Worker Configuration**: Web Push requires a service worker (`sw.js`) that must specifically `importScripts('https://assets.magicbell.io/web-push-notifications/sw.js')`. Path issues are common.
*   **React Headless Deprecation**: The recent deprecation of `@magicbell/react-headless` in favor of the unified `@magicbell/react` package can cause confusion for developers following older tutorials. [Discussion](https://github.com/orgs/magicbell/discussions/265)
*   **Channel Overrides complexity**: Customizing content per channel (e.g., a short SMS vs. a rich HTML email) requires a nested `overrides` object in the API payload which is prone to schema errors.
## 5. Evaluation Ideas
*   **Basic Integration**: Add a `FloatingInbox` to a navigation bar and trigger a test notification from the dashboard.
*   **Secure Auth Implementation**: Create a Node.js/Express endpoint that signs a User JWT correctly and provides it to a React frontend.
*   **Custom UI Rendering**: Implement a custom notification item using the `ItemComponent` prop to display avatars and action buttons.
*   **Web Push Setup**: Configure a service worker and add a `WebPushButton` that successfully registers a browser for push notifications.
*   **Multi-Channel Logic**: Send a broadcast that uses `overrides` to provide a different `action_url` for Slack vs. Email.
*   **Preference Management**: Build a "Notification Settings" page using the `UserPreferences` component and verify it updates the user's delivery rules.
## 6. Sources
1.  [MagicBell Documentation Home](https://www.magicbell.com/docs) - Core documentation portal.
2.  [MagicBell Quick Start](https://www.magicbell.com/docs/quick-start) - Initial setup and broadcast guide.
3.  [React SDK Reference](https://www.magicbell.com/docs/libraries/magicbell-react) - Detailed props and usage for React components.
4.  [User JWT Authentication](https://www.magicbell.com/docs/api/authentication/user) - Security and token generation details.
5.  [API v2 Reference](https://www.magicbell.com/docs/api/reference) - Full REST API specification.
6.  [MagicBell GitHub Discussions](https://github.com/orgs/magicbell/discussions) - Community questions and friction points.
7.  [Notification Primitive](https://www.magicbell.com/docs/primitive/notification) - Lifecycle and states of notifications.