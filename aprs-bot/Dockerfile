FROM python:3.7-alpine

COPY requirements.txt /tmp/requirements.txt

RUN apk add build-base --no-cache
RUN pip install -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt
RUN apk del build-base

COPY src/* /app/

CMD python /app/aprs-bot.py