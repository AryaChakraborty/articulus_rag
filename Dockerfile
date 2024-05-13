# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV MONGO_URL <your_mongo_url>
ENV GOOGLE_API_KEY <your_google_api_key>

# Run app.py when the container launches
CMD ["python", "app.py"]
