#!/bin/sh

# Wait for the database to be ready
/wait-for-it.sh db:5432 --timeout=30

# Initialize the database
python app/init_db.py

# Dump environment variables to a file
printenv > /etc/default/locale

# Write out current crontab
crontab -l > mycron

# Cron job to send output to Docker container logs
echo "0 * * * * . /etc/default/locale; echo 'Cron job started at $(date)' >> /proc/1/fd/1; /usr/local/bin/python /app/parse_postfix_logs.py >> /proc/1/fd/1 2>> /proc/1/fd/2; echo 'Cron job ended at $(date)' >> /proc/1/fd/1" >> mycron


# Install new cron file
crontab mycron
rm mycron


# Start the cron service
service cron start

# Start the Uvicorn server
uvicorn app.main:app --host "0.0.0.0" --port "8000" --forwarded-allow-ips '*'
