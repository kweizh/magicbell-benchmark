# MagicBell Notification Badge Customization

## Background
You have a React application using MagicBell's `FloatingInbox`. By default, the trigger button is a bell icon. You need to customize this trigger button (often referred to as the notification badge) by providing a custom `ButtonComponent`.

## Requirements
- Create a custom button component to replace the default MagicBell trigger.
- The custom button must be a `<button>` element with the ID `custom-bell-btn`.
- The button text must be `My Alerts`.
- The button must correctly receive and use the `onClick` and `ref` props so that clicking it toggles the inbox.
- Apply this custom component to the `FloatingInbox` in `src/App.jsx`.

## Implementation Guide
1. Open `/home/user/app/src/App.jsx`.
2. Define a new component (e.g., `CustomButton`) using `React.forwardRef` to handle the `ref` and `onClick` props.
3. Return `<button id="custom-bell-btn" onClick={onClick} ref={ref}>My Alerts</button>`.
4. Pass your new component to the `ButtonComponent` prop of the `<FloatingInbox />`.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: `3000`