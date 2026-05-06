const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;
const logFile = path.join(__dirname, 'magicbell_events.log');

app.use(express.json());

app.post('/webhooks/magicbell', (req, res) => {
  const { event, notification, user } = req.body;

  if (event === 'notification_read' && notification && user) {
    const logEntry = `${notification.id} read by ${user.email}\n`;
    fs.appendFileSync(logFile, logEntry);
  }

  res.status(200).send('OK');
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
