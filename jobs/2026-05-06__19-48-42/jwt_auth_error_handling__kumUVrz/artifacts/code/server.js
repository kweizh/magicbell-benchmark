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
      { 
        user_email: email,
        api_key: MAGICBELL_API_KEY
      },
      MAGICBELL_API_SECRET,
      { algorithm: 'HS256' }
    );
    res.json({ token });
  } catch (err) {
    res.status(500).json({ error: 'Failed to generate token' });
  }
});

app.listen(3001, () => {
  console.log('Backend running on port 3001');
});
