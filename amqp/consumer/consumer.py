#!/usr/bin/env python3
"""
AMQP Consumer for RabbitMQ
Consumes joke messages from a RabbitMQ queue using AMQP protocol.
"""

import os
import time
from datetime import datetime

import pika


def callback(ch, method, properties, body):
    """Callback function to process received messages."""
    timestamp = datetime.now()
    message = body.decode()
    print(f"[{timestamp}] Received message:")
    print(f"[{timestamp}] {message}")
    print(f"[{timestamp}] Delivery tag: {method.delivery_tag}")
    print("-" * 80)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """Main consumer loop."""
    # Get configuration from environment variables
    host = os.getenv("RABBITMQ_HOST", "localhost")
    port = int(os.getenv("RABBITMQ_PORT", "5672"))
    user = os.getenv("RABBITMQ_USER", "guest")
    password = os.getenv("RABBITMQ_PASS", "guest")
    queue_name = os.getenv("QUEUE_NAME", "jokes_queue")

    print(f"[{datetime.now()}] AMQP Consumer starting...")
    print(f"[{datetime.now()}] RabbitMQ: {host}:{port}")
    print(f"[{datetime.now()}] Queue: {queue_name}")

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
        blocked_connection_timeout=300,
    )

    while True:
        try:
            # Create connection and channel
            print(f"[{datetime.now()}] Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Declare queue (idempotent operation)
            channel.queue_declare(queue=queue_name, durable=True)
            print(f"[{datetime.now()}] Connected successfully")

            # Set QoS to process one message at a time
            channel.basic_qos(prefetch_count=1)

            # Set up consumer
            channel.basic_consume(
                queue=queue_name, on_message_callback=callback, auto_ack=False
            )

            print(f"[{datetime.now()}] Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()

        except KeyboardInterrupt:
            print(f"\n[{datetime.now()}] Consumer stopped by user")
            try:
                channel.stop_consuming()
                connection.close()
            except Exception:
                pass
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f"[{datetime.now()}] Connection error: {e}")
            print(f"[{datetime.now()}] Reconnecting in 5 seconds...")
            time.sleep(5)
        except pika.exceptions.AMQPChannelError as e:
            print(f"[{datetime.now()}] Channel error: {e}")
            print(f"[{datetime.now()}] Reconnecting in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"[{datetime.now()}] Unexpected error: {e}")
            print(f"[{datetime.now()}] Reconnecting in 5 seconds...")
            time.sleep(5)
        finally:
            try:
                if "connection" in locals() and connection.is_open:
                    connection.close()
            except Exception as e:
                print(f"[{datetime.now()}] Error closing connection: {e}")

    print(f"[{datetime.now()}] Consumer shutdown complete")


if __name__ == "__main__":
    main()
