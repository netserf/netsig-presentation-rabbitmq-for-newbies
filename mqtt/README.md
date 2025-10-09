# RabbitMQ MQTT Docker Test Environment

This directory contains a Docker-based test environment for RabbitMQ with MQTT
protocol support, providing a message broker with MQTT-enabled producer and
consumer clients for testing and demonstrating MQTT messaging capabilities.

## Version Information

- **RabbitMQ Version**: 4.1.4-management
- **Upgraded**: October 2025

## Overview

The environment consists of:

- A RabbitMQ server with MQTT plugin enabled
- A producer client that publishes MQTT messages to topics
- A consumer client that subscribes to MQTT topics and receives messages
- Management UI for monitoring and administration
- Configuration for MQTT protocol on port 1883

This setup uses **Docker Compose** to orchestrate all containers, providing a
cleaner and more maintainable configuration compared to individual container
commands.

## ⚠️ Security Notice

**This is a demonstration environment for educational purposes.**

The credentials used in this demo (`admin/YodaSaysUseStrongPwd9!`) are
intentionally simple and publicly visible in the docker-compose.yml file.
These are suitable for local demos and learning only.

**Never use these credentials in production environments.** For production use,
implement proper secrets management using Docker secrets, environment files,
or a secrets management service.

## Environment Details

- Base Image: RabbitMQ 4.1.4 with Management
- Containers:
  - `rabbitmq-server`: Message broker with MQTT plugin enabled
  - `mqtt-producer`: Client that publishes test messages to MQTT topics
  - `mqtt-consumer`: Client that subscribes to MQTT topics and receives messages
- Networking: All containers are on a custom Docker network (`rabbitmq-net`)
- Protocols:
  - MQTT on port 1883
  - Management UI on port 15672 (<http://localhost:15672>, guest/guest)
- Message Flow: Producer → RabbitMQ (topic: demo/topic) → Consumer

## Key Differences vs AMQP

- Uses MQTT protocol instead of AMQP
- Simpler topic-based messaging (no complex routing keys)
- Uses `paho-mqtt` library instead of `pika`
- Messages are typically transient (weaker persistence/durability)
- Less control over transactions and advanced routing
- Ideal for IoT and lightweight messaging scenarios

## Prerequisites

- Docker installed
- Docker Compose (included with Docker Desktop, or install separately)

## Make Options

The following make targets are available for managing the environment:

- `make build`: Builds all container images using Docker Compose
- `make up`: Starts all containers in detached mode
- `make down`: Stops and removes all containers and networks
- `make ps`: Lists running containers
- `make logs`: Shows logs from all containers (follow mode)
- `make logs-server`: Shows logs from the RabbitMQ server
- `make logs-producer`: Shows logs from the producer
- `make logs-consumer`: Shows logs from the consumer
- `make exec-server`: Opens a shell in the server container
- `make exec-producer`: Opens a shell in the producer container
- `make exec-consumer`: Opens a shell in the consumer container
- `make restart`: Restarts all containers
- `make restart-server`: Restarts only the RabbitMQ server
- `make restart-producer`: Restarts only the producer
- `make restart-consumer`: Restarts only the consumer
- `make mgmt`: Opens the RabbitMQ management UI in browser
- `make clean`: Stops containers and removes images

## Quick Start

1. Build the images:

   ```bash
   make build
   ```

2. Start the environment:

   ```bash
   make up
   ```

3. View the logs to see messages being published and consumed:

   ```bash
   make logs-producer
   make logs-consumer
   ```

4. Access the management UI:

   ```bash
   make mgmt
   ```

   Or navigate to <http://localhost:15672> (username: guest, password: guest)

5. Stop the environment:

   ```bash
   make down
   ```

## Architecture

```text
┌─────────────┐         MQTT (1883)        ┌──────────────────┐
│   Producer  │ ──────────────────────────>│  RabbitMQ Server │
│             │    publish to demo/topic   │  (MQTT enabled)  │
└─────────────┘                            └──────────────────┘
                                                     │
                                                     │ MQTT (1883)
                                                     │ subscribe to demo/topic
                                                     ▼
                                            ┌─────────────┐
                                            │  Consumer   │
                                            └─────────────┘

All containers connected via rabbitmq-net Docker network
```

## Configuration

### RabbitMQ Server

- MQTT plugin enabled at startup
- Default credentials: guest/guest
- Management UI enabled on port 15672
- Runs with `--rm` flag (container removed on stop)

### Producer

- Publishes messages to `demo/topic` every 5 seconds
- Uses `paho-mqtt` Python library
- Connects to `rabbitmq-server:1883`
- Configurable via environment variables

### Consumer

- Subscribes to `demo/topic`
- Uses `paho-mqtt` Python library
- Prints received messages to stdout
- Connects to `rabbitmq-server:1883`
- Configurable via environment variables

## Docker Compose Features

This setup uses Docker Compose for orchestration:

- Declarative configuration in `docker-compose.yml`
- Automatic network creation and management
- Service dependencies with health checks
- Simplified container lifecycle management
- Compatible with Docker and Docker
- Easy to extend and modify service configurations

### Key Benefits Over Individual Commands

- **Simplified Management**: Single command to start/stop all services
- **Dependency Handling**: Producer and consumer wait for RabbitMQ health check
- **Declarative Config**: All settings in one YAML file
- **Reproducible**: Easy to version control and share
- **Scalable**: Simple to add more services or replicas

## Extending the Environment

### Adding TLS/MQTTS Support

To enable TLS (MQTTS on port 8883):

1. Generate or obtain SSL certificates
2. Update the `make up` target to expose port 8883
3. Mount certificates into the RabbitMQ container with `-v` flags
4. Configure RabbitMQ MQTT plugin for TLS
5. Update producer/consumer to use TLS connection

### Adding More Topics

Modify the producer and consumer Python scripts to publish/subscribe to
additional topics as needed. You can run multiple producers/consumers with
different topic configurations.

### Custom Message Formats

Update the producer script to send JSON, binary, or other message formats as
required by your use case.

## Troubleshooting

### Containers won't start

- Ensure no other services are using ports 1883, 5672, or 15672
- Check if containers from previous runs are still active: `docker ps -a`
- Try `make clean` followed by `make build` and `make up`
- Verify Docker Compose is installed: `docker compose version`

### Can't connect to Management UI

- Verify the server is running: `make ps`
- Check server logs: `make logs-server`
- Ensure port 15672 is not blocked by firewall

### Messages not being received

- Check both producer and consumer logs: `make logs`
- Verify all containers are running: `make ps`
- The health check ensures RabbitMQ is ready before clients start
- Check RabbitMQ server logs for connection issues: `make logs-server`

### Docker Compose not found

If you get a "command not found" error:

- **Docker Desktop users**: Docker Compose is included, ensure Docker Desktop is running
- **Linux users**: Install Docker Compose plugin:

  ```bash
  sudo apt-get install docker-compose-plugin
  ```

- Or use the standalone version: `docker-compose` (note the hyphen)
