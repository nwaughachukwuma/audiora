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
    xclip \
    xsel \
    gtk \
    && rm -rf /var/lib/apt/lists/*
    
RUN xclip -version
RUN xsel --version
    
COPY . ./
    
# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=:0
RUN python3 -c "import pyperclip; pyperclip.copy('test'); print(pyperclip.paste())"

ENV HOST '0.0.0.0'
EXPOSE $PORT
HEALTHCHECK CMD curl --fail http://$HOST:$PORT/_stcore/health

CMD exec streamlit run app.py --server.port=$PORT --server.address=$HOST
