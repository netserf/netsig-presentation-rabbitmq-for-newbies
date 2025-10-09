# Use Python slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install pika (RabbitMQ client)
RUN pip install --no-cache-dir pika

# Copy the consumer script
COPY consumer.py .

# Run the consumer
CMD ["python", "-u", "consumer.py"]
