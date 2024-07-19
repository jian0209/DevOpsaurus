#! /bin/bash
set -x

# Start the application
echo "Starting the application..."

# use supervisord to start the application
supervisord -c /etc/supervisor/conf.d/supervisord.conf &

# initialize the database
echo "Initializing the database..."
mysql -h$DATABASE_URL -u"$DATABASE_USERNAME" -p"$DATABASE_PASSWORD" --database=$DATABASE_NAME < /app/server/init_database.sql

# initialize the admin
echo "Initializing data..."

while ! nc -z localhost 9001; do
  sleep 1
done

curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:9001/api/v1/user/init_admin
curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:9001/api/v1/settings/init

echo "Done initialization."
echo "Application started."

tail -f /dev/null
