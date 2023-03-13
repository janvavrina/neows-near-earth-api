#!/bin/bash

if [ -z "$1" ]; then
    API_KEY="DEMO_KEY"
else
    API_KEY="$1"
fi

echo "API_KEY=$API_KEY" > .env
