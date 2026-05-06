const jwt = require('jsonwebtoken');

async function updatePreferences() {
  const apiKey = process.env.MAGICBELL_API_KEY;
  const apiSecret = process.env.MAGICBELL_API_SECRET;
  const apiUrl = process.env.MAGICBELL_API_URL;

  if (!apiKey || !apiSecret || !apiUrl) {
    console.error('Missing environment variables: MAGICBELL_API_KEY, MAGICBELL_API_SECRET, or MAGICBELL_API_URL');
    process.exit(1);
  }

  const userEmail = 'user@example.com';

  // Generate User JWT
  const token = jwt.sign(
    {
      user_email: userEmail,
      api_key: apiKey,
    },
    apiSecret,
    { algorithm: 'HS256' }
  );

  const requestBody = {
    categories: [
      {
        key: 'updates',
        channels: [
          { name: 'email', enabled: false }
        ]
      }
    ]
  };

  try {
    const response = await fetch(`${apiUrl}/channels/user_preferences`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    console.log(`Status Code: ${response.status}`);
    
    if (!response.ok) {
        const errorData = await response.text();
        console.error('Error Response:', errorData);
    }
  } catch (error) {
    console.error('Request failed:', error);
  }
}

updatePreferences();
