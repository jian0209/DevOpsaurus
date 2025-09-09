FROM node:20-alpine3.21 AS frontend-builder
WORKDIR /build
COPY . .
RUN npm install \
  && npm install -g quasar-cli \
  && npm run build

FROM python:3.9-slim AS backend
WORKDIR /app

COPY server /app/server
COPY --from=frontend-builder /build/dist/spa/* /app/client
COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

# install mysql client, curl, netcat only if truly needed at runtime
RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
    curl \
    default-mysql-client \
    netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r /app/server/requirement.txt

ENV FLASK_APP=/app/server/app.py

EXPOSE 9000
EXPOSE 9001

CMD ["/app/start.sh"]
