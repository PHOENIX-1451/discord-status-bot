# Python version
FROM python:3.12-slim

# Working directory inside container
WORKDIR /app

# Copy requirements.txt to container (for dependencies)
COPY ./requirements.txt /app

# Unbuffered logging
ENV PYTHONUNBUFFERED=1

# API request base interval
ENV BASE_REFRESH_INTERVAL=10

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy scripts to /app
COPY . /app

# Execute command to start the app
CMD ["python", "main.py"]