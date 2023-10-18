#!/bin/sh

# Wait for the database to be ready
/wait-for-it.sh db:5432 --timeout=30

# Initialize the database
python app/init_db.py

# Start the Uvicorn server
uvicorn app.main:app --host "0.0.0.0" --port "8000" --forwarded-allow-ips '*'
