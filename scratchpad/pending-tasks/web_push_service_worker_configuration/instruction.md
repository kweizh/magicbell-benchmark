Enabling web push notifications in MagicBell requires a dedicated service worker. Pathing and configuration issues are frequent friction points for developers setting this up.

You need to configure a web push service worker by creating a `sw.js` file in a generic frontend project's public directory and registering it appropriately in the main JavaScript entry point.

**Constraints:**
- The `sw.js` file MUST contain exactly the following import script statement: `importScripts('https://assets.magicbell.io/web-push-notifications/sw.js')`.
- The main application entry file must check for `'serviceWorker' in navigator` before attempting to register `sw.js`.
- The service worker file must be placed at the absolute root of the server (`/sw.js`) to ensure maximum scope.