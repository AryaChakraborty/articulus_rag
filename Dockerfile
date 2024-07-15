# Stage 1: Build stage
FROM python:3.10-slim as builder

# Setting the working directory in the builder
WORKDIR /app

# Copying contents into the builder container
COPY . /app

# Copying env variables into builder container.
COPY .env /app/.env

# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.10-slim AS final

# Setting the working directory in the final container
WORKDIR /app

# Copying only the necessary files from the builder stage
COPY --from=builder /app /app

# Using port 5000
EXPOSE 5000

# Environment variables from .env file are loaded in app.py

# Run app.py when the container launches
CMD ["python", "app.py"]
