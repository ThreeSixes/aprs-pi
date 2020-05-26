FROM python:3.7-alpine

COPY requirements.txt /tmp/requirements.txt

ENV APRS_BOT_ENABLED=true
ENV DEBUG=false
ENV KISS_CONN_TYPE=tcp
ENV KISS_HOST=127.0.0.1
ENV KISS_PORT=6700
ENV MQTT_TOPIC_PREFIX=aprs
ENV MQTT_PORT=1883
ENV MQTT_SERVER=127.0.0.1

RUN apk add build-base --no-cache
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt
RUN apk del build-base

COPY src/* /app/

CMD python /app/aprs-bot.py