MagicBell acts as the notification layer in modern web applications, providing a pre-built UI to display user alerts. The unified `@magicbell/react` package simplifies rendering this UI within a React application.

You need to integrate the MagicBell notification inbox into an existing React application's navigation bar by utilizing the `MagicBellProvider` and `FloatingInbox` components. 

**Constraints:**
- Must use the unified `@magicbell/react` package (do NOT use the deprecated `@magicbell/react-headless` package).
- Must initialize `MagicBellProvider` with a provided `API_KEY` and a hardcoded `userJwt` token.
- Must render the `FloatingInbox` component correctly inside the `MagicBellProvider` context without any custom overrides.