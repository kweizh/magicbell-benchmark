#!/bin/bash

# Ensure required environment variables are set
if [ -z "$MAGICBELL_API_KEY" ]; then
    echo "Error: MAGICBELL_API_KEY environment variable is not set." >&2
    exit 1
fi

if [ -z "$MAGICBELL_USER_EMAIL" ]; then
    echo "Error: MAGICBELL_USER_EMAIL environment variable is not set." >&2
    exit 1
fi

# Make the POST request to mark all notifications as read
curl -s -X POST https://api.magicbell.com/notifications/read \
     -H "X-MAGICBELL-API-KEY: $MAGICBELL_API_KEY" \
     -H "X-MAGICBELL-USER-EMAIL: $MAGICBELL_USER_EMAIL" \
     -H "Content-Type: application/json" \
     -d '{}'
