# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install paho-mqtt library and pyjokes
RUN pip install --no-cache-dir paho-mqtt==2.1.0 pyjokes

# Copy the producer script
COPY producer.py .

# Run the producer
CMD ["python", "-u", "producer.py"]
