# RabbitMQ AMQP Demo

A demonstration of RabbitMQ messaging using the AMQP protocol with Python
producer and consumer applications.

## Version Information

- **RabbitMQ Version**: 4.1.4-management
- **Upgraded**: October 2025

## Overview

This demo showcases:

- **RabbitMQ Server**: Message broker with management UI
- **AMQP Producer**: Python application that publishes messages to a queue
- **AMQP Consumer**: Python application that consumes and displays messages
  from the queue

## ⚠️ Security Notice

**This is a demonstration environment for educational purposes.**

The credentials used in this demo (`admin/YodaSaysUseStrongPwd9!`) are
intentionally simple and publicly visible in the docker-compose.yml file.
These are suitable for local demos and learning only.

**Never use these credentials in production environments.** For production use,
implement proper secrets management using Docker secrets, environment files,
or a secrets management service.

## Architecture

```text
┌─────────────────┐
│  AMQP Producer  │
│                 │
└────────┬────────┘
         │ AMQP (port 5672)
         │ Publishes messages
         ▼
┌─────────────────┐
│  RabbitMQ       │
│  Server         │
│  (message queue)│
└────────┬────────┘
         │ AMQP (port 5672)
         │ Delivers messages
         ▼
┌─────────────────┐
│  AMQP Consumer  │
│  (displays)     │
└─────────────────┘
```

## Features

- **Persistent Messages**: Messages are marked as durable and persistent
- **Manual Acknowledgment**: Consumer manually acknowledges messages after
  processing
- **Quality of Service**: Consumer processes one message at a time
- **Auto-reconnection**: Both producer and consumer automatically reconnect on
  connection failures

## Prerequisites

- Docker and Docker Compose
- Make (optional, for convenience commands)

## Quick Start

### Using Make

```bash
# Build all images
make build

# Start all containers
make up

# View logs from all containers
make logs

# View producer logs only
make logs-producer

# View consumer logs only
make logs-consumer

# Open RabbitMQ Management UI
make ui

# Stop all containers
make down

# Clean up (stop and remove images)
make clean
```

### Using Docker Compose Directly

```bash
# Build and start
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

## Configuration

Environment variables can be modified in `docker-compose.yml`:

### Producer Configuration

- `RABBITMQ_HOST`: RabbitMQ server hostname (default: `rabbitmq-server`)
- `RABBITMQ_PORT`: AMQP port (default: `5672`)
- `RABBITMQ_USER`: Username (default: `guest`)
- `RABBITMQ_PASS`: Password (default: `guest`)
- `QUEUE_NAME`: Queue name (default: `jokes_queue`)
- `PUBLISH_INTERVAL`: Seconds between messages (default: `15`)

### Consumer Configuration

- `RABBITMQ_HOST`: RabbitMQ server hostname (default: `rabbitmq-server`)
- `RABBITMQ_PORT`: AMQP port (default: `5672`)
- `RABBITMQ_USER`: Username (default: `guest`)
- `RABBITMQ_PASS`: Password (default: `guest`)
- `QUEUE_NAME`: Queue name (default: `jokes_queue`)

## RabbitMQ Management UI

Access the management interface at:

- **URL**: <http://localhost:15672>
- **Username**: `guest`
- **Password**: `guest`

The management UI allows you to:

- Monitor queue depth and message rates
- View active connections and channels
- Inspect message details
- Manage exchanges, queues, and bindings

## Project Structure

```text
docker/rabbitmq/amqp/
├── docker-compose.yml      # Container orchestration
├── Makefile               # Convenience commands
├── README.md              # This file
├── producer/
│   ├── Dockerfile         # Producer container image
│   └── producer.py        # Producer application
└── consumer/
    ├── Dockerfile         # Consumer container image
    └── consumer.py        # Consumer application
```

## How It Works

### Producer

1. Connects to RabbitMQ using AMQP protocol
1. Declares a durable queue
1. Generates and publishes messages every 15 seconds
1. Marks messages as persistent
1. Automatically reconnects on connection failures

### Consumer

1. Connects to RabbitMQ using AMQP protocol
1. Declares the same durable queue
1. Sets QoS to process one message at a time
1. Consumes messages and displays them
1. Manually acknowledges each message after processing
1. Automatically reconnects on connection failures

## AMQP vs MQTT

This demo uses AMQP instead of MQTT. Key differences:

| Feature | AMQP | MQTT |
|---------|------|------|
| Protocol | Advanced Message Queuing Protocol | Message Queuing Telemetry Transport |
| Use Case | Enterprise messaging, complex routing | IoT, lightweight messaging |
| Message Model | Queue-based | Topic-based (pub/sub) |
| QoS Levels | Acknowledgments, transactions | 0, 1, 2 |
| Overhead | Higher | Lower |

## Troubleshooting

### Producer/Consumer Not Connecting

Check RabbitMQ server health:

```bash
docker compose logs rabbitmq-server
```

### No Messages Being Received

1. Check producer is publishing:

   ```bash
   make logs-producer
   ```

1. Check queue in management UI at <http://localhost:15672>

1. Verify consumer is connected:

   ```bash
   make logs-consumer
   ```

### Port Conflicts

If ports 15672 or 5672 are already in use, modify the port mappings in
`docker-compose.yml`.

## Development

### Modifying the Producer

Edit `producer/producer.py` and rebuild:

```bash
make build
make restart-producer
```

### Modifying the Consumer

Edit `consumer/consumer.py` and rebuild:

```bash
make build
make restart-consumer
```

## Python Dependencies

- **pika**: RabbitMQ client library for Python

## License

This is a demonstration project for educational purposes.

## Related Demos

- **MQTT Demo**: See `docker/rabbitmq/mqtt/` for MQTT protocol example
