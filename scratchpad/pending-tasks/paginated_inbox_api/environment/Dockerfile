FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl wget ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="MagicBell paginated inbox API task environment"

RUN mkdir -p /home/user/magicbell-task && \
    cd /home/user/magicbell-task && \
    cat > mock_server.js <<'EOF'
const http = require('http');
const url = require('url');

const notifications = [
  { id: 'n1', title: 'Notif 1' },
  { id: 'n2', title: 'Notif 2' },
  { id: 'n3', title: 'Notif 3' },
  { id: 'n4', title: 'Notif 4' },
  { id: 'n5', title: 'Notif 5' }
];

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);
  
  if (req.method === 'GET' && parsedUrl.pathname === '/v2/notifications') {
    const authHeader = req.headers['authorization'] || req.headers['x-magicbell-user-jwt'];
    if (!authHeader) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      return res.end(JSON.stringify({ errors: [{ message: 'Unauthorized' }] }));
    }

    const limit = parseInt(parsedUrl.query.limit) || 50;
    const startingAfter = parsedUrl.query.starting_after;

    let startIndex = 0;
    if (startingAfter) {
      const idx = notifications.findIndex(n => n.id === startingAfter);
      if (idx !== -1) {
        startIndex = idx + 1;
      }
    }

    const result = notifications.slice(startIndex, startIndex + limit);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ notifications: result }));
  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(8080, () => {
  console.log('Mock server listening on port 8080');
});
EOF

# Container contents:
#   - Node.js v24 installed.
#   - /home/user/magicbell-task: Project directory.
#   - /home/user/magicbell-task/mock_server.js: Mock server for MagicBell API.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]