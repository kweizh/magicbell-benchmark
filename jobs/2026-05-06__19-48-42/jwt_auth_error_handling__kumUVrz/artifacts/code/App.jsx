import React, { useState, useEffect } from 'react';
import MagicBellProvider from '@magicbell/react/context-provider';
import FloatingInbox from '@magicbell/react/floating-inbox';

export default function App() {
  const [token, setToken] = useState(null);
  const [error, setError] = useState(false);
  const email = 'test@example.com';

  useEffect(() => {
    fetch(`http://localhost:3001/api/token?email=${email}`)
      .then(res => {
        if (!res.ok) {
          throw new Error('Authentication failed');
        }
        return res.json();
      })
      .then(data => {
        if (data.token) {
          setToken(data.token);
        } else {
          setError(true);
        }
      })
      .catch(() => {
        setError(true);
      });
  }, []);

  if (error) {
    return <div id="error-message">Authentication failed</div>;
  }

  if (!token) return <div>Loading...</div>;

  return (
    <MagicBellProvider apiKey="test_api_key" userJwt={token}>
      <FloatingInbox />
    </MagicBellProvider>
  );
}
