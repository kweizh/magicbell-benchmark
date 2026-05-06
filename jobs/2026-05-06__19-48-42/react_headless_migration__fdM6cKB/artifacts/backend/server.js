const express = require('express');
const cors = require('cors');
const jwt = require('jsonwebtoken');

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

app.get('/auth', (req, res) => {
  const payload = {
    user_email: 'test@example.com'
  };
  const secret = 'SUPER_SECRET_KEY';
  const token = jwt.sign(payload, secret, { algorithm: 'HS256' });
  res.json({ token });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
