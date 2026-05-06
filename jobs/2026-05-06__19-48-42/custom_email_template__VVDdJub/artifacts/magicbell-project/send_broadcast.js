const axios = require('axios');

const MAGICBELL_API_KEY = 'dummy_key';
const MAGICBELL_API_SECRET = 'dummy_secret';

async function sendBroadcast() {
  const url = 'https://api.magicbell.com/v2/broadcasts';
  const payload = {
    broadcast: {
      title: "Welcome to our platform",
      recipients: [
        { email: "newuser@example.com" }
      ],
      overrides: {
        channels: {
          email: {
            title: "Welcome Email",
            html: "<h1>Welcome!</h1><p>Thanks for joining.</p>"
          }
        }
      }
    }
  };

  const config = {
    headers: {
      'X-MAGICBELL-API-KEY': MAGICBELL_API_KEY,
      'X-MAGICBELL-API-SECRET': MAGICBELL_API_SECRET,
      'Content-Type': 'application/json'
    }
  };

  try {
    const response = await axios.post(url, payload, config);
    console.log('Broadcast sent successfully:');
    console.log(JSON.stringify(response.data, null, 2));
  } catch (error) {
    console.error('Error sending broadcast:');
    if (error.response) {
      console.error(JSON.stringify(error.response.data, null, 2));
    } else {
      console.error(error.message);
    }
  }
}

sendBroadcast();
