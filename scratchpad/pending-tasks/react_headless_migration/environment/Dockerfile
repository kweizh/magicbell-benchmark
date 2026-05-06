FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="React app using deprecated @magicbell/react-headless, and an empty backend directory."

RUN mkdir -p /home/user/magicbell-backend && \
    cd /home/user && \
    npx create-vite@latest magicbell-migration --template react && \
    cd /home/user/magicbell-migration && \
    npm install && \
    npm install @magicbell/react-headless@5.5.1

RUN cd /home/user/magicbell-migration && \
    cat > src/App.jsx <<'EOF'
import React from 'react';
import { MagicBellProvider } from '@magicbell/react-headless';

function App() {
  return (
    <MagicBellProvider apiKey="dummy-api-key" userEmail="test@example.com">
      <div>
        <h1>Notifications</h1>
      </div>
    </MagicBellProvider>
  );
}

export default App;
EOF

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/magicbell-backend - empty directory for backend setup.
#   - /home/user/magicbell-migration - React app with @magicbell/react-headless installed and used in App.jsx.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]