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
    ffmpeg \
    libcairo2-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . ./
# RUN rm -rf ./app

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pycairo

ENV HOST '0.0.0.0'
ENV WORKER 4
ENV THREADS 16
ENV TIMEOUT 0

EXPOSE 8080

CMD exec gunicorn -k uvicorn.workers.UvicornWorker -b :$PORT -w $WORKER --threads $THREADS -t $TIMEOUT --preload server.src.main:app
