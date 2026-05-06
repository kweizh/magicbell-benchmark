const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

app.use(express.json());

app.post('/webhook/stripe', async (req, res) => {
  const event = req.body;

  if (event.type === 'invoice.payment_succeeded') {
    const dataObject = event.data.object;
    const subscriptionId = dataObject.subscription;
    const customerEmail = dataObject.customer_email;

    const magicbellApiUrl = process.env.MAGICBELL_API_URL || 'https://api.magicbell.com';
    const magicbellApiKey = process.env.MAGICBELL_API_KEY;
    const magicbellApiSecret = process.env.MAGICBELL_API_SECRET;

    try {
      await axios.post(
        `${magicbellApiUrl}/broadcasts`,
        {
          broadcast: {
            title: 'Payment Successful',
            content: `Your payment for subscription ${subscriptionId} was successful.`,
            recipients: [{ email: customerEmail }],
          },
        },
        {
          headers: {
            'X-MAGICBELL-API-KEY': magicbellApiKey,
            'X-MAGICBELL-API-SECRET': magicbellApiSecret,
            'Content-Type': 'application/json',
          },
        }
      );
      console.log(`MagicBell broadcast sent for subscription ${subscriptionId}`);
    } catch (error) {
      console.error('Error sending MagicBell broadcast:', error.response ? error.response.data : error.message);
      // We still return 200 to Stripe to acknowledge receipt of the webhook, 
      // but in a real scenario we might want to handle retries or logging.
    }
  }

  res.status(200).send('Webhook received');
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
