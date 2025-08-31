#!/bin/bash

# Cron entrypoint script
echo "Starting cron service..."

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "Database is unavailable - sleeping"
  sleep 1
done
echo "Database is up - setting up cron"

# Create cron log file
touch /app/logs/cron.log

# Create cron job script
cat > /app/run_crons.sh << 'EOF'
#!/bin/bash
cd /app
echo "$(date): Running Django cron jobs..." >> /app/logs/cron.log
python manage.py runcrons >> /app/logs/cron.log 2>&1
EOF

chmod +x /app/run_crons.sh

# Add cron job to run every minute
echo "* * * * * /app/run_crons.sh" > /etc/cron.d/django-cron

# Give execution rights on the cron job
chmod 0644 /etc/cron.d/django-cron

# Apply cron job
crontab /etc/cron.d/django-cron

# Create the log file to be able to run tail
touch /var/log/cron.log

# Start cron daemon
echo "Starting cron daemon..."
cron

# Keep the container running and show cron logs
echo "Cron service started. Tailing logs..."
tail -f /app/logs/cron.log