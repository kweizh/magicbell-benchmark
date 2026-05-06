#!/bin/bash

curl -X POST https://api.magicbell.com/v2/broadcasts \
     -H "X-MAGICBELL-API-KEY: $MAGICBELL_API_KEY" \
     -H "X-MAGICBELL-API-SECRET: $MAGICBELL_API_SECRET" \
     -H "Content-Type: application/json" \
     -d '{
       "broadcast": {
         "title": "Welcome!",
         "content": "Click here to get started.",
         "action_url": "https://example.com/start",
         "recipients": [
           {
             "email": "test@example.com"
           }
         ]
       }
     }' > /home/user/output.json
