# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

WORKDIR /gitcomp

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip to the latest version
RUN pip3 install --no-cache-dir --upgrade pip

# Create and activate a virtual environment
RUN python3 -m venv venv

# Install the Python dependencies in the virtual environment
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["/bin/bash", "-c", "source venv/bin/activate && flask run"]

