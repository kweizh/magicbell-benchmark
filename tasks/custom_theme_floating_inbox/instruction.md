# Custom Theme for MagicBell Floating Inbox

## Background
MagicBell's React SDK allows customization of its UI components using CSS variables. In this task, you will integrate the `FloatingInbox` into a React application and apply a custom dark theme.

## Requirements
- Create a React application.
- Install `@magicbell/react`.
- Render the `FloatingInbox` component wrapped in a MagicBell `Provider` using a dummy token.
- Create a custom stylesheet `src/theme.css` that sets MagicBell's CSS variables on the `body` selector to create a dark theme.
  - Set `--magicbell-bg-default` to `#111827`.
  - Set `--magicbell-text-default` to `#f5f5f5`.
- Import the custom stylesheet in your main application file.

## Implementation Guide
1. Initialize a new React project in `/home/user/myproject` (e.g., using `npm create vite@latest . -- --template react-ts`).
2. Install `@magicbell/react`.
3. Create `src/theme.css` with the required CSS variables.
4. Update `src/App.tsx` (or `src/App.jsx`) to import `@magicbell/react/styles/floating-inbox.css`, `src/theme.css`, and render the `FloatingInbox` within a `Provider` (use `token="dummy_token"`).

## Constraints
- Project path: `/home/user/myproject`
- Start command: `npm run dev -- --host`
- Port: 5173