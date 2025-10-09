# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install paho-mqtt library
RUN pip install --no-cache-dir paho-mqtt==2.1.0

# Copy the consumer script
COPY consumer.py .

# Run the consumer
CMD ["python", "-u", "consumer.py"]
