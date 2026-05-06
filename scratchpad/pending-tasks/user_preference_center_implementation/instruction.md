MagicBell provides built-in mechanisms for users to manage their notification preferences, allowing them to opt-out of specific channels (like SMS or Email) for certain categories of notifications without writing backend logic.

You need to build a "Notification Settings" React page that renders the MagicBell `UserPreferences` component, allowing the authenticated user to toggle their delivery rules across different channels.

**Constraints:**
- The `UserPreferences` component must be wrapped inside a securely authenticated `MagicBellProvider`.
- Provide a structured layout that renders the preference UI inside a container with a maximum width of `800px`.
- Do not attempt to build custom toggles; you must rely entirely on the native `UserPreferences` component's UI.