import { MagicBellProvider, FloatingInbox } from '@magicbell/react';
import '@magicbell/react/styles/floating-inbox.css';
import './theme.css';
import './App.css';

function App() {
  return (
    <MagicBellProvider
      apiKey="dummy_api_key"
      userEmail="dummy@example.com"
      token="dummy_token"
    >
      <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#111827' }}>
        <h1 style={{ color: '#f5f5f5' }}>MagicBell Dark Theme Demo</h1>
        <FloatingInbox />
      </div>
    </MagicBellProvider>
  );
}

export default App;
