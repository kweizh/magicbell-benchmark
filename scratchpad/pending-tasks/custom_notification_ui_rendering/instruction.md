While MagicBell's default inbox is fully functional, developers frequently need to match the notification UI to their application's specific design system, such as displaying custom user avatars or specific action buttons.

You need to implement a custom notification item inside the `FloatingInbox` component by utilizing the `ItemComponent` prop in a React environment. 

**Constraints:**
- The custom component must receive notification data and render both the notification `title` and a placeholder avatar image.
- Do not modify the default styling of the `FloatingInbox` container itself, only the individual notification items.
- Ensure the custom component correctly displays unread states based on the notification data passed to it.