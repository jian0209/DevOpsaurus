FROM python:3.9-slim

RUN apt-get update && \
  apt-get install -y nodejs npm && \
  npm install -g quasar-cli && \
  apt-get install -y default-mysql-client curl netcat-traditional

WORKDIR /app

COPY server /app/server
COPY . /app/build
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

RUN pip install --no-cache-dir -r /app/server/requirement.txt

ENV FLASK_APP=/app/server/app.py

EXPOSE 9000
EXPOSE 9001

CMD ["/app/start.sh"]
