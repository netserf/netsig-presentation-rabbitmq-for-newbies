# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install pika (RabbitMQ client) and pyjokes
RUN pip install --no-cache-dir pika pyjokes

# Copy the producer script
COPY producer.py .

# Run the producer
CMD ["python", "-u", "producer.py"]
