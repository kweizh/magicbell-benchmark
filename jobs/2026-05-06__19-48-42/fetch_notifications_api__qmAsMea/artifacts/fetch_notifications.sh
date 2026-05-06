#!/bin/bash
curl -X GET "https://api.magicbell.com/v2/notifications" \
     -H "Authorization: Bearer dummy_user_jwt_token" \
     -H "Accept: application/json"
