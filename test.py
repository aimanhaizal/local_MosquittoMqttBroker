import paho.mqtt.client as mqtt
import time
import random
import string

# MQTT broker details
broker = "172.17.0.1"
port = 1884
topic = "test/topic"

# Generate a 60-byte payload (random string of 60 characters)
def generate_payload():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=60))

# Set up MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker, port, 60)

# Start the loop to handle network traffic
client.loop_start()

try:
    while True:
        payload = generate_payload()  # Generate 60-byte payload
        client.publish(topic, payload)  # Publish to the broker
        print(f"Sent: {payload}")  # Print the sent payload (optional)
        time.sleep(1)  # Wait for 1 second before sending the next message

except KeyboardInterrupt:
    print("Terminating the publisher.")

finally:
    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect from the broker

# change the code to take the data from the csv files with qos = 1