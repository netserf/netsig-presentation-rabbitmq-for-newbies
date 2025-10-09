#!/usr/bin/env python3
"""
AMQP Producer for RabbitMQ
Publishes joke messages to a RabbitMQ queue using AMQP protocol.
"""

import os
import time
import sys
from datetime import datetime

import pika
import pyjokes


def main():
    """Main producer loop."""
    # Get configuration from environment variables
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_PORT", "5672"))
    user = os.getenv("RABBITMQ_USER", "guest")
    password = os.getenv("RABBITMQ_PASS", "guest")
    queue_name = os.getenv("QUEUE_NAME", "jokes_queue")
    interval = int(os.getenv("PUBLISH_INTERVAL", "5"))

    print(f"[{datetime.now()}] AMQP Producer starting...")
    print(f"[{datetime.now()}] RabbitMQ: {host}:{port}")
    print(f"[{datetime.now()}] Queue: {queue_name}")
    print(f"[{datetime.now()}] Publish interval: {interval} seconds")

    # Wait for RabbitMQ to be ready
    print(f"[{datetime.now()}] Waiting for RabbitMQ to be ready...")
    time.sleep(10)

    # Set up connection parameters
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )

    message_count = 0

    try:
        while True:
            try:
                # Create connection and channel
                print(f"[{datetime.now()}] Connecting to RabbitMQ...")
                connection = pika.BlockingConnection(parameters)
                channel = connection.channel()

                # Declare queue (idempotent operation)
                channel.queue_declare(queue=queue_name, durable=True)
                print(f"[{datetime.now()}] Connected successfully")

                # Publish messages
                while True:
                    message_count += 1
                    timestamp = datetime.now().isoformat()
                    joke = pyjokes.get_joke()
                    message = f"Joke #{message_count} at {timestamp}: {joke}"

                    channel.basic_publish(
                        exchange='',
                        routing_key=queue_name,
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode=2,  # Make message persistent
                        )
                    )
                    print(f"[{datetime.now()}] Published: {message}")
                    time.sleep(interval)

            except pika.exceptions.AMQPConnectionError as e:
                print(f"[{datetime.now()}] Connection error: {e}")
                print(f"[{datetime.now()}] Reconnecting in 5 seconds...")
                time.sleep(5)
            except pika.exceptions.AMQPChannelError as e:
                print(f"[{datetime.now()}] Channel error: {e}")
                print(f"[{datetime.now()}] Reconnecting in 5 seconds...")
                time.sleep(5)
            finally:
                try:
                    if 'connection' in locals() and connection.is_open:
                        connection.close()
                except Exception as e:
                    print(f"[{datetime.now()}] Error closing connection: {e}")

    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Producer stopped by user")
    except Exception as e:
        print(f"[{datetime.now()}] Unexpected error: {e}")
        sys.exit(1)
    finally:
        print(f"[{datetime.now()}] Producer shutdown complete")


if __name__ == "__main__":
    main()
