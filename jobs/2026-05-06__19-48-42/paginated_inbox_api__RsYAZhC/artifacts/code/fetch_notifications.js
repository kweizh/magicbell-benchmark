const jwt = require('jsonwebtoken');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

const API_KEY = process.env.MAGICBELL_API_KEY;
const API_SECRET = process.env.MAGICBELL_API_SECRET;
const API_URL = process.env.MAGICBELL_API_URL || 'https://api.magicbell.com/v2';
const USER_EMAIL = 'test_user@example.com';
const OUTPUT_FILE = path.join(__dirname, 'output.json');

if (!API_KEY || !API_SECRET) {
  console.error('MAGICBELL_API_KEY and MAGICBELL_API_SECRET environment variables are required.');
  process.exit(1);
}

function generateJWT() {
  const payload = {
    user_email: USER_EMAIL,
    api_key: API_KEY
  };
  return jwt.sign(payload, API_SECRET, { algorithm: 'HS256' });
}

async function fetchAllNotifications() {
  const userJwt = generateJWT();
  const titles = [];
  let startingAfter = null;
  const limit = 2;

  try {
    while (true) {
      let url = `${API_URL}/notifications?limit=${limit}`;
      if (startingAfter) {
        url += `&starting_after=${startingAfter}`;
      }

      console.log(`Fetching: ${url}`);
      const response = await axios.get(url, {
        headers: {
          'X-MAGICBELL-USER-JWT': userJwt,
          'X-MAGICBELL-API-KEY': API_KEY
        }
      });

      const notifications = response.data.notifications;
      if (!notifications || notifications.length === 0) {
        break;
      }

      notifications.forEach(n => titles.push(n.title));
      startingAfter = notifications[notifications.length - 1].id;
    }

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(titles, null, 2));
    console.log(`Successfully fetched ${titles.length} notifications and saved to ${OUTPUT_FILE}`);
  } catch (error) {
    console.error('Error fetching notifications:', error.response ? error.response.data : error.message);
    process.exit(1);
  }
}

fetchAllNotifications();
