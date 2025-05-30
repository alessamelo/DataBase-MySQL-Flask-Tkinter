# Dockerfile
FROM python:3.11-slim

# Install build dependencies needed for cryptography
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app .

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

CMD ["python", "app.py"]