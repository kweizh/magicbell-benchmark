FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages requests PyJWT

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="MagicBell JWT Authentication task environment with React and Express."

RUN mkdir -p /home/user/magicbell-app/src && \
    cd /home/user/magicbell-app && \
    cat >package.json <<'EOF'
{
  "name": "magicbell-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "concurrently \"node server.js\" \"vite\"",
    "build": "vite build"
  },
  "dependencies": {
    "@magicbell/react": "^1.0.0",
    "express": "^4.18.2",
    "jsonwebtoken": "^9.0.0",
    "cors": "^2.8.5",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "concurrently": "^8.0.0",
    "vite": "^4.3.9"
  }
}
EOF

RUN cd /home/user/magicbell-app && \
    cat >server.js <<'EOF'
const express = require('express');
const jwt = require('jsonwebtoken');
const cors = require('cors');

const app = express();
app.use(cors());

const MAGICBELL_API_KEY = process.env.MAGICBELL_API_KEY || 'test_api_key';
const MAGICBELL_API_SECRET = process.env.MAGICBELL_API_SECRET || 'test_api_secret';

app.get('/api/token', (req, res) => {
  const { email } = req.query;
  
  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  // BUG 1: using 'email' instead of 'user_email'
  // BUG 2: missing 'api_key'
  // BUG 3: using 'RS256' instead of 'HS256'
  try {
    const token = jwt.sign(
      { email: email },
      MAGICBELL_API_SECRET,
      { algorithm: 'RS256' }
    );
    res.json({ token });
  } catch (err) {
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

app.listen(3001, () => {
  console.log('Backend running on port 3001');
});
EOF

RUN cd /home/user/magicbell-app && \
    cat >src/App.jsx <<'EOF'
import React, { useState, useEffect } from 'react';
import MagicBellProvider from '@magicbell/react/context-provider';
import FloatingInbox from '@magicbell/react/floating-inbox';

export default function App() {
  const [token, setToken] = useState(null);
  const email = 'test@example.com';

  useEffect(() => {
    fetch(`http://localhost:3001/api/token?email=${email}`)
      .then(res => res.json())
      .then(data => {
        if (data.token) {
          setToken(data.token);
        }
      });
  }, []);

  if (!token) return <div>Loading...</div>;

  return (
    <MagicBellProvider apiKey="test_api_key" userJwt={token}>
      <FloatingInbox />
    </MagicBellProvider>
  );
}
EOF

RUN cd /home/user/magicbell-app && \
    cat >index.html <<'EOF'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>MagicBell App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOF

RUN cd /home/user/magicbell-app && \
    cat >src/main.jsx <<'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOF

RUN cd /home/user/magicbell-app && \
    cat >vite.config.js <<'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
})
EOF

RUN cd /home/user/magicbell-app && npm install

ENV MAGICBELL_API_KEY="test_api_key"
ENV MAGICBELL_API_SECRET="test_api_secret"

# Container contents:
#   - Node.js v24 for the MagicBell task environment
#   - /home/user/magicbell-app: React app with Express backend containing the JWT auth bugs

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
