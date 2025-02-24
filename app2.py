import paho.mqtt.client as mqtt
import json

# MQTT parameters for Mosquitto broker
MOSQUITTO_BROKER = "10.1.43.8"
MOSQUITTO_PORT = 1884
MOSQUITTO_TOPIC = "test/topic"

# MQTT parameters for ThingsBoard
THINGSBOARD_BROKER = "10.1.43.8"
THINGSBOARD_PORT = 1883
THINGSBOARD_TOPIC = "v1/devices/me/telemetry"
THINGSBOARD_USERNAME = "yed_Dishwasher"  # Device token

# Global ThingsBoard client
thingsboard_client = None

def on_message(client, userdata, msg):
    try:
        # Decode the received message
        received_data = msg.payload.decode("utf-8")
        print(f"Received data: {received_data}")

        # Attempt to parse the received data as JSON
        data = json.loads(received_data)

        # Publish the received data to ThingsBoard
        global thingsboard_client
        payload = json.dumps(data)
        thingsboard_client.publish(THINGSBOARD_TOPIC, payload, qos=1)
        print(f"Published data to ThingsBoard: {data}")

    except Exception as e:
        print(f"Error processing message: {e}")

def on_disconnect(client, userdata, rc):
    """Callback for when the client disconnects from the broker."""
    print(f"Disconnected from broker with result code: {rc}")
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        client.reconnect()

def main():
    global thingsboard_client

    # Set up the Mosquitto client
    mosquitto_client = mqtt.Client()
    mosquitto_client.on_message = on_message

    # Connect to the Mosquitto broker and subscribe to the topic
    mosquitto_client.connect(MOSQUITTO_BROKER, MOSQUITTO_PORT, 60)
    mosquitto_client.subscribe(MOSQUITTO_TOPIC, qos=1)

    # Set up the ThingsBoard client
    thingsboard_client = mqtt.Client()
    thingsboard_client.username_pw_set(THINGSBOARD_USERNAME)
    thingsboard_client.on_disconnect = on_disconnect  # Handle disconnections
    thingsboard_client.connect(THINGSBOARD_BROKER, THINGSBOARD_PORT, 60)

    # Start the network loop for both clients
    mosquitto_client.loop_start()
    thingsboard_client.loop_start()

    print("Listening for messages...")

    try:
        # Keep the script running
        while True:
            pass
    except KeyboardInterrupt:
        print("Script interrupted. Disconnecting clients...")
        mosquitto_client.loop_stop()
        thingsboard_client.loop_stop()
        mosquitto_client.disconnect()
        thingsboard_client.disconnect()

if __name__ == "__main__":
    main()
