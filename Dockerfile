FROM python:3.7.1-slim

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
