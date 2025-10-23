#!/usr/bin/env python3
"""
MQTT Consumer for RabbitMQ
Subscribes to a specified MQTT topic and prints received messages.
"""

import os
import time
import sys
from datetime import datetime

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc, properties=None):
    """Callback when connected to MQTT broker."""
    if rc == 0:
        print(f"[{datetime.now()}] Connected to MQTT broker successfully")
        # Subscribe to topic after successful connection
        topic = userdata.get("topic", "demo/topic")
        client.subscribe(topic, qos=1)
        print(f"[{datetime.now()}] Subscribed to topic: {topic}")
    else:
        print(f"[{datetime.now()}] Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    """Callback when a message is received."""
    timestamp = datetime.now()
    payload = msg.payload.decode()

    # Extract just the joke from the message
    # Message format: "Message #X from producer at TIMESTAMP : JOKE"
    if " : " in payload:
        joke = payload.split(" : ", 1)[1]
    else:
        joke = payload

    print(f"\n[{timestamp}] Message received: {joke}\n")


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """Callback when subscription is confirmed."""
    print(f"[{datetime.now()}] Subscription confirmed (mid: {mid}, QoS: {granted_qos})")


def main():
    """Main consumer loop."""
    # Get configuration from environment variables
    broker = os.getenv("MQTT_BROKER", "rabbitmq-server")
    port = int(os.getenv("MQTT_PORT", "1883"))
    username = os.getenv("MQTT_USER", "guest")
    password = os.getenv("MQTT_PASS", "guest")
    topic = os.getenv("MQTT_TOPIC", "demo/topic")

    print(f"[{datetime.now()}] MQTT Consumer starting...")
    print(f"[{datetime.now()}] Broker: {broker}:{port}")
    print(f"[{datetime.now()}] Username: {username}")
    print(f"[{datetime.now()}] Topic: {topic}")

    # Create MQTT client with userdata containing topic
    userdata = {"topic": topic}
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2, client_id="mqtt-consumer", userdata=userdata
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

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

    # Start the loop to process callbacks
    print(f"[{datetime.now()}] Starting message loop...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now()}] Consumer stopped by user")
    except Exception as e:
        print(f"[{datetime.now()}] Error: {e}")
    finally:
        client.disconnect()
        print(f"[{datetime.now()}] Consumer shutdown complete")


if __name__ == "__main__":
    main()
