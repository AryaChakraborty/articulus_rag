# Using an official Python runtime as a parent image (3.9 version)
FROM python:3.9-slim

# Setting the working directory in the container
WORKDIR /app

# Copying contents into the container
COPY . /app

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Using port 5000
EXPOSE 5000

# Environment variables from .env file are loaded in app.py

# Run app.py when the container launches
CMD ["python", "app.py"]
