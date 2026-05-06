const fs = require('fs');

const payload = {
  broadcast: {
    title: 'Alert',
    content: 'System down',
    action_url: 'https://example.com/alert',
    recipients: [
      {
        email: 'admin@example.com'
      }
    ],
    overrides: {
      channels: {
        slack: {
          action_url: 'https://example.com/slack-alert'
        }
      }
    }
  }
};

fs.writeFileSync('payload.json', JSON.stringify(payload, null, 2));
console.log('payload.json has been generated.');
