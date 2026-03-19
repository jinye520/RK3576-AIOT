FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pyserial paho-mqtt

COPY main.py /app/main.py
COPY entrypoint.sh /app/entrypoint.sh
COPY config.example.json /app/config.example.json

RUN chmod +x /app/entrypoint.sh

CMD ["sh", "/app/entrypoint.sh"]
