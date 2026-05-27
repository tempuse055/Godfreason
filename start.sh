#!/bin/bash
# Start the API in background
gunicorn api:app --bind 0.0.0.0:$PORT --workers 1 --timeout 30 &
# Start the Telegram bot
python3 drx.py
