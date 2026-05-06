#!/bin/bash

# Default MAGICBELL_API_URL if not set
BASE_URL=${MAGICBELL_API_URL:-https://api.magicbell.com}

# Remove trailing slash if present
BASE_URL=${BASE_URL%/}

# Endpoint
ENDPOINT="/v2/integrations/twilio"
URL="${BASE_URL}${ENDPOINT}"

# Check for required environment variables
if [[ -z "$MAGICBELL_API_KEY" || -z "$MAGICBELL_API_SECRET" || -z "$TWILIO_ACCOUNT_SID" || -z "$TWILIO_API_KEY" || -z "$TWILIO_API_SECRET" || -z "$TWILIO_FROM_NUMBER" ]]; then
  echo "Error: One or more required environment variables are missing."
  echo "Required: MAGICBELL_API_KEY, MAGICBELL_API_SECRET, TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_FROM_NUMBER"
  exit 1
fi

# Send PUT request
curl -X PUT "$URL" \
     -H "X-MAGICBELL-API-KEY: $MAGICBELL_API_KEY" \
     -H "X-MAGICBELL-API-SECRET: $MAGICBELL_API_SECRET" \
     -H "Content-Type: application/json" \
     -d @- <<EOF
{
  "account_sid": "$TWILIO_ACCOUNT_SID",
  "api_key": "$TWILIO_API_KEY",
  "api_secret": "$TWILIO_API_SECRET",
  "from": "$TWILIO_FROM_NUMBER"
}
EOF
