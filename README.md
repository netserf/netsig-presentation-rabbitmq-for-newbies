# 🔔 NetSIG Presentation - Playing with Pub/Sub

Welcome to *Playing with Pub/Sub*! This repository contains a presentation and
demos designed to introduce you to the world of **publish/subscribe messaging**
using **RabbitMQ** with both **MQTT** and **AMQP** protocols.

Whether you're a developer curious about message queuing, building IoT
applications, or designing distributed systems, this repo will help you
understand the fundamentals of pub/sub messaging patterns.

[![Actions Status](https://github.com/netserf/netsig-presentation-playing-with-pub-sub/workflows/Lint/badge.svg)](https://github.com/netserf/netsig-presentation-playing-with-pub-sub/actions)

## 📦 Contents

- `slides/`: Presentation slides (PDF)
- `mqtt/`: MQTT protocol demo with RabbitMQ
- `amqp/`: AMQP protocol demo with RabbitMQ

## 👥 Who is this for?

- Developers new to message queuing and pub/sub patterns
- IoT hobbyists or engineers looking to understand MQTT messaging
- Backend developers interested in asynchronous communication
- Anyone wanting to learn RabbitMQ fundamentals
- Teams evaluating message broker solutions

## 🎯 What you'll learn

- What pub/sub messaging is and why it's useful
- Key differences between MQTT and AMQP protocols
- How to set up and run RabbitMQ with Docker
- Building simple producer/consumer applications
- When to use MQTT vs AMQP for your use case
- Message broker concepts: topics, queues, exchanges
- Hands-on demos you can run locally

## 🧰 Prerequisites

- Basic knowledge of networking and messaging concepts
- Familiarity with the Linux command line
- Docker and Docker Compose installed
- Basic Python knowledge (for understanding demo code)

## 🎤 Presentation

The slide deck is available here:
📽️ [netsig-playing-with-pub-sub.pdf](slides/netsig-playing-with-pub-sub.pdf)

## ⚠️ Security Notice

**This is a demonstration repository for educational purposes.**

The credentials in the Docker Compose files (`admin/YodaSaysUseStrongPwd9!`) are
intentionally simple and publicly visible. These are suitable for local demos
only.

**Never use these credentials in production environments.**

## 🚀 Quick Start

### MQTT Demo (Lightweight, IoT-focused)

Perfect for beginners! MQTT is simple, lightweight, and ideal for IoT scenarios.

```bash
cd mqtt
make build
make up
make logs
```

Access RabbitMQ Management UI: <http://localhost:15672>\
(username: `admin`, password: `YodaSaysUseStrongPwd9!`)

**Note:** These are demo credentials for local testing only.

See the [MQTT README](mqtt/README.md) for detailed instructions.

### AMQP Demo (Enterprise messaging)

More advanced protocol with complex routing and guaranteed delivery.

```bash
cd amqp
make build
make up
make logs
```

Access RabbitMQ Management UI: <http://localhost:15672>\
(username: `guest`, password: `guest`)

**Note:** These are demo credentials for local testing only.

See the [AMQP README](amqp/README.md) for detailed instructions.

## 🔍 MQTT vs AMQP - Quick Comparison

| Feature | MQTT | AMQP |
|---------|------|------|
| **Use Case** | IoT, lightweight messaging | Enterprise messaging, complex routing |
| **Protocol Overhead** | Low | Higher |
| **Message Model** | Topic-based (pub/sub) | Queue-based with exchanges |
| **QoS Levels** | 0, 1, 2 | Acknowledgments, transactions |
| **Typical Port** | 1883 (8883 for TLS) | 5672 (5671 for TLS) |
| **Best For** | Sensors, mobile apps, constrained devices | Microservices, enterprise integration |
| **Complexity** | Simple | More complex, more features |

## 🛠️ Demo Architecture

Both demos follow a similar pattern:

```text
┌─────────────┐         Protocol          ┌──────────────────┐
│  Producer   │ ─────────────────────────>│  RabbitMQ Server │
│             │   publish messages        │  (message broker)│
└─────────────┘                           └──────────────────┘
                                                   │
                                                   │ Protocol
                                                   │ subscribe/consume
                                                   ▼
                                            ┌─────────────┐
                                            │  Consumer   │
                                            └─────────────┘
```

### MQTT Demo Features

- Publishes programming jokes to `demo/topic`
- Simple topic-based routing
- QoS level 1 (at least once delivery)
- Automatic reconnection on failures
- Uses `paho-mqtt` Python library

### AMQP Demo Features

- Publishes jokes to `jokes_queue`
- Persistent messages with durability
- Manual acknowledgments
- Quality of Service (one message at a time)
- Uses `pika` Python library

## 🛜 Who is NetSIG?

NetSIG is a Special Interest Group focused on computer networking. We're
affiliated with Victoria Raspberry PiMakers group located in Victoria, Canada.
These presentations are hosted in person and online.

## ❓ Where can I find more on NetSIG and presentation schedules?

- [NetSIG site](https://vicpimakers.ca/netsig/)
- [Victoria PiMakers site](https://vicpimakers.ca/)

## 🙏 Feedback

Spotted a typo? Got a better way to explain a concept? Have suggestions for
improvements? I'd love your feedback! Open an issue or pull request 🛠️

## 🧠 Acknowledgements

- [RabbitMQ Project](https://www.rabbitmq.com/) – the excellent message broker
- [Paho MQTT](https://www.eclipse.org/paho/) – MQTT client library
- [Pika](https://pika.readthedocs.io/) – AMQP client library for Python
- [PyJokes](https://pyjok.es/) – for keeping our demos entertaining

## 🪪 License

[![CC BY 4.0](https://licensebuttons.net/l/by/4.0/88x31.png)](https://creativecommons.org/licenses/by/4.0/)

This content is licensed under the Creative Commons Attribution 4.0
International License.
