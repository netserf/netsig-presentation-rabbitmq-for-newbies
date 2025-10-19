# Start with the official RabbitMQ image with management plugin
FROM rabbitmq:4.1.4-management

# Set environment variable to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install useful networking tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        nmap \
        netcat-openbsd \
        dnsutils \
        iproute2 \
        iputils-ping \
        traceroute \
        tcpdump \
        mosquitto-clients && \
    rm -rf /var/lib/apt/lists/*

# Enable MQTT plugin
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt

# Copy custom RabbitMQ configuration for MQTT broadcast behavior
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

# Expose the necessary ports
# AMQP
EXPOSE 5672
# Management UI
EXPOSE 15672
# MQTT
EXPOSE 1883
# MQTTS (TLS)
EXPOSE 8883

# Use the default RabbitMQ entrypoint
CMD ["rabbitmq-server"]
