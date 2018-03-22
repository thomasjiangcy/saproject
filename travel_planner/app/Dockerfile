# python image using Debian Stretch
FROM python:3.6-slim-stretch

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip3 install -U pip && pip3 install -r /app/requirements.txt

COPY . /app
RUN chmod +x /app/scripts/start-app.sh

