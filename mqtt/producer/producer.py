#!/usr/bin/env python3
"""
MQTT Producer for RabbitMQ
Publishes messages to a specified MQTT topic at regular intervals.
"""

import os
import time
import sys
from datetime import datetime

import paho.mqtt.client as mqtt
import pyjokes


def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker."""
    if rc == 0:
        print(f"[{datetime.now()}] Connected to MQTT broker successfully")
    else:
        print(f"[{datetime.now()}] Failed to connect, return code {rc}")


def on_publish(client, userdata, mid, reason_code=None, properties=None):
    """Callback when message is published."""
    print(f"[{datetime.now()}] Message published (mid: {mid})")


def main():
    """Main producer loop."""
    # Get configuration from environment variables
    broker = os.getenv("MQTT_BROKER", "rabbitmq-server")
    port = int(os.getenv("MQTT_PORT", "1883"))
    username = os.getenv("MQTT_USER", "guest")
    password = os.getenv("MQTT_PASS", "guest")
    topic = os.getenv("MQTT_TOPIC", "demo/topic")
    interval = int(os.getenv("PUBLISH_INTERVAL", "5"))

    print(f"[{datetime.now()}] MQTT Producer starting...")
    print(f"[{datetime.now()}] Broker: {broker}:{port}")
    print(f"[{datetime.now()}] Username: {username}")
    print(f"[{datetime.now()}] Topic: {topic}")
    print(f"[{datetime.now()}] Publish interval: {interval} seconds")

    # Create MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt-producer")
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Set username and password
    client.username_pw_set(username, password)

    # Wait for broker to be ready
    print(f"[{datetime.now()}] Waiting for broker to be ready...")
    time.sleep(10)

    # Connect to broker
    try:
        print(f"[{datetime.now()}] Connecting to broker...")
        client.connect(broker, port, 60)
    except Exception as e:
        print(f"[{datetime.now()}] Error connecting to broker: {e}")
        sys.exit(1)

    # Publish messages in a loop with proper network loop handling
    message_count = 0
    try:
        # Start the network loop in background
        client.loop_start()

        while True:
            time.sleep(interval)
            message_count += 1
            timestamp = datetime.now().isoformat()
            joke = pyjokes.get_joke()
            message = (
                f"Message #{message_count} from producer at " f"{timestamp} : {joke}"
            )

            print(f"[{datetime.now()}] Publishing: {message}")
            result = client.publish(topic, message, qos=1)

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"[{datetime.now()}] Failed to publish message")
            else:
                # Wait for message to be sent
                result.wait_for_publish()

    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Producer stopped by user")
    except Exception as e:
        print(f"[{datetime.now()}] Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print(f"[{datetime.now()}] Producer shutdown complete")


if __name__ == "__main__":
    main()
