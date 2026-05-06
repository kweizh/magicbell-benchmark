import React, { useEffect, useState } from 'react';
import MagicBellProvider from '@magicbell/react/context-provider';
import Inbox from '@magicbell/react/inbox';
import '@magicbell/react/styles/inbox.css';

function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    fetch('http://localhost:3001/auth')
      .then((res) => res.json())
      .then((data) => setToken(data.token))
      .catch((err) => console.error('Error fetching token:', err));
  }, []);

  if (!token) {
    return <div>Loading...</div>;
  }

  return (
    <MagicBellProvider token={token}>
      <div>
        <h1>Notifications</h1>
        <Inbox />
      </div>
    </MagicBellProvider>
  );
}

export default App;
