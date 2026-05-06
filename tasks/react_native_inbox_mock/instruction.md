# React Native Inbox Mock

## Background
You need to build a mock MagicBell inbox for a React Native application that runs on Expo Web. Since the official React SDK is optimized for web, you will use the MagicBell REST API directly to fetch and display notifications in a React Native `FlatList`.

## Requirements
- Initialize a React Native app using Expo in `/home/user/myproject` (already done).
- Implement a component that fetches notifications from the MagicBell API `GET https://api.magicbell.com/notifications`.
- Use the provided `X-MAGICBELL-API-KEY` and `X-MAGICBELL-USER-EMAIL` headers to authenticate.
- Render the notifications in a `FlatList`.
- Each notification should display its `title` and `content`.
- Add a "Mark all as read" button that calls `POST https://api.magicbell.com/notifications/read`.

## Implementation Guide
1. Modify `App.js` in `/home/user/myproject` to include the inbox component.
2. Use `fetch` to call the MagicBell REST API.
3. Ensure the app runs correctly on Expo Web.

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npx expo start --web --port 3000`
- Port: 3000
- Use `FlatList` for rendering.