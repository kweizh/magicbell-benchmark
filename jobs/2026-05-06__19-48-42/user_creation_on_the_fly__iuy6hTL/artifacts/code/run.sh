#!/bin/bash
curl -s -X POST https://api.magicbell.com/v2/broadcasts \
     -H "X-MAGICBELL-API-KEY: dummy_key" \
     -H "X-MAGICBELL-API-SECRET: dummy_secret" \
     -H "Content-Type: application/json" \
     -d '{
  "broadcast": {
    "title": "Welcome",
    "content": "Hello new user",
    "recipients": [
      {
        "email": "new_user_on_the_fly@example.com"
      }
    ]
  }
}'
