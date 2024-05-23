# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /gitcomp

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip3 install --no-cache-dir --upgrade pip

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]
