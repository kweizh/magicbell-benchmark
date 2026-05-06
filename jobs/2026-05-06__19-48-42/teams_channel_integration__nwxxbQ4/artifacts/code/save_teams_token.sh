#!/bin/bash

# Exit non-zero if arguments are missing
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <USER_JWT> <WEBHOOK_URL>"
    exit 1
fi

USER_JWT=$1
WEBHOOK_URL=$2

# Use MAGICBELL_API_URL if set, otherwise use default
API_URL=${MAGICBELL_API_URL:-"https://api.magicbell.com/v2"}

# Construct JSON payload
PAYLOAD=$(cat <<EOF
{
  "webhook": {
    "url": "$WEBHOOK_URL"
  }
}
EOF
)

# Send PUT request
curl -X PUT \
     -H "Authorization: Bearer $USER_JWT" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD" \
     "$API_URL/channels/teams/tokens"
