#! /bin/bash
set -e

# mv from app_bak to app
if [ ! -d "/app/server" ]; then
    cp -r /app_bak/* /app
fi
rm -rf /app_bak

: "${WEB_URL:=http://localhost}"
find /app/client -type f -name '*.js' | xargs sed -i "s|__WEB_URL__|$WEB_URL|g"

# initialize the database
OUTPUT=$(mysql -h$DATABASE_URL -u$DATABASE_USERNAME -p$DATABASE_PASSWORD --skip-ssl --database=information_schema -e "SELECT COUNT(*) FROM tables WHERE table_schema = '$DATABASE_NAME'" -s)
if [ $OUTPUT -eq 0 ]; then
    echo "Initializing the database..."
    sed -i "s/__DB__/$DATABASE_NAME/g" /app/server/init_database.sql
    sed -i "s/__DB_USER__/$DATABASE_USERNAME/g" /app/server/init_database.sql
    sed -i "s/__DB_PASSWORD__/$DATABASE_PASSWORD/g" /app/server/init_database.sql

    mysql -h$DATABASE_URL -u$DATABASE_USERNAME -p$DATABASE_PASSWORD --skip-ssl --database=$DATABASE_NAME < /app/server/init_database.sql
    rm /app/server/init_database.sql
fi


# Start the application
echo "Starting the application..."

# use supervisord to start the application
cd /app/server
flask run --host=0.0.0.0 --port=9001 >> /dev/stdout 2>&1 &
backend_pid=$!

cd /app/client
quasar serve --port 9000 >> /dev/stdout 2>&1 &
frontend_pid=$!
# supervisord -c /etc/supervisor/conf.d/supervisord.conf &

while ! nc -z localhost 9001; do
    echo "Waiting for the application to start..."
    sleep 1
done

# get data from mysql and set to variable
OUTPUT=$(mysql -h$DATABASE_URL -u$DATABASE_USERNAME -p$DATABASE_PASSWORD --skip-ssl --database=$DATABASE_NAME -e "SELECT COUNT(*) FROM d_user_info" -s)
if [ $OUTPUT -eq 0 ]; then
    echo "Initializing data..."
    curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:9001/api/v1/user/init_admin
    curl -X POST -H "Content-Type: application/json" -d '{}' http://localhost:9001/api/v1/settings/init
    echo "Done initialization."
fi

echo "Application started."

while true; do
    sleep 3
    if ! kill -0 $backend_pid > /dev/null 2>&1; then
        echo "backend has exited" > /dev/stdout
        break
    fi
    if ! kill -0 $frontend_pid > /dev/null 2>&1; then
        echo "frontend has exited" > /dev/stdout
        break
    fi
done

