#!/bin/bash

# Check if API key is set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY environment variable is not set"
    exit 1
fi

# Check if a prompt was provided
if [ -z "$1" ]; then
    echo "Usage: $0 \"Your prompt here\""
    exit 1
fi

PROMPT="$1"

# Make the API call
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d "{
    \"contents\": [
      {
        \"parts\": [
          {
            \"text\": \"$PROMPT\"
          }
        ]
      }
    ]
  }" | jq -r '.candidates[0].content.parts[0].text' 