# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.12-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install FFmpeg, Cairo, and any other required dependencies
RUN apt-get -yqq update && apt-get -yqq install \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
COPY . ./
# RUN rm -rf ./api
    
# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt 

ENV HOST '0.0.0.0'
EXPOSE $PORT
CMD exec gunicorn -b :$PORT main:app
