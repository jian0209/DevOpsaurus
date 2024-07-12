FROM python:3.9-slim

RUN apt-get update && \
  apt-get install -y nodejs npm && \
  npm install -g serve && \
  apt-get install -y supervisor

WORKDIR /app

COPY server /app/server
COPY . /app/client

RUN pip install --no-cache-dir -r /app/server/requirement.txt

WORKDIR /app/client

RUN npm install

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV FLASK_APP=/app/server/app.py

# Start supervisord to manage the processes
CMD ["/usr/bin/supervisord"]
