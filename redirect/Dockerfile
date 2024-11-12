FROM python:3.12-slim

ENV PYTHONUNBUFFERED True
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get -yqq update && apt-get -yqq install \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
    
COPY . ./
    
# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt 

ENV HOST '0.0.0.0'
EXPOSE $PORT
CMD exec gunicorn -b :$PORT main:app
