#!/bin/bash

# Check if environment variables are set
if [ -z "$MAGICBELL_API_KEY" ] || [ -z "$MAGICBELL_API_SECRET" ]; then
  echo "Error: MAGICBELL_API_KEY and MAGICBELL_API_SECRET environment variables must be set."
  exit 1
fi

curl -X POST https://api.magicbell.com/v2/broadcasts \
  -H "X-MAGICBELL-API-KEY: $MAGICBELL_API_KEY" \
  -H "X-MAGICBELL-API-SECRET: $MAGICBELL_API_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "broadcast": {
      "title": "System Alert",
      "content": "General alert message",
      "recipients": [
        {
          "email": "user@example.com"
        }
      ],
      "overrides": {
        "slack": {
          "content": "Slack-specific alert message"
        }
      }
    }
  }'
