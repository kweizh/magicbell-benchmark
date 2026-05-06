import React from 'react';
import MagicBellProvider from '@magicbell/react/context-provider';
import FloatingInbox from '@magicbell/react/floating-inbox';

const CustomButton = React.forwardRef((props, ref) => {
  return (
    <button id="custom-bell-btn" onClick={props.onClick} ref={ref}>
      My Alerts
    </button>
  );
});

function App() {
  return (
    <MagicBellProvider token="DUMMY_TOKEN">
      <FloatingInbox ButtonComponent={CustomButton} />
    </MagicBellProvider>
  );
}

export default App;
