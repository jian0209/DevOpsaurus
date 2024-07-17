#! /bin/bash
set -e

# Start the application
echo "Starting the application..."

# use supervisord to start the application
supervisord -c /etc/supervisor/conf.d/supervisord.conf &

# initialize the database
mysql -h$DATABASE_URL -u$DATABASE_USERNAME -p$DATABASE_PASSWORD --database$DATABASE_NAME < /app/server/init_database.sql

# initialize the admin
curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:9001/v1/user/init_admin

echo "Done initialization."
echo "Application started."
disown
