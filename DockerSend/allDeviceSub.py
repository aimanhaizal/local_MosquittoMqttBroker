import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

load_dotenv()

# MQTT parameters for Mosquitto broker
MOSQUITTO_BROKER = os.getenv("MOSQUITTO_BROKER")
MOSQUITTO_PORT = int(os.getenv("MOSQUITTO_PORT"))
MOSQUITTO_TOPIC = os.getenv("MOSQUITTO_TOPIC")

# MQTT parameters for ThingsBoard
THINGSBOARD_BROKER = os.getenv("THINGSBOARD_BROKER")
THINGSBOARD_PORT = int(os.getenv("THINGSBOARD_PORT"))
THINGSBOARD_TOPIC = os.getenv("THINGSBOARD_TOPIC")

# Device-specific ThingsBoard access tokens
devices = {
    "00Fridge": "yed_Fridge",
    "01CoffeeMaker": "yed_CoffeeMaker",
    "02Oven": "yed_Oven",
    "03InductionCooker": "yed_InductionCooker",
    "05AirConditionerPanasonic_CoffeeMaker": "yed_AirConditionerPanasonic",
    "06AirConditionerPanasonic_InductionCooker": "yed_Dishwasher",
}

# Global ThingsBoard clients
thingsboard_clients = {}

def on_message(client, userdata, msg):
    try:
        # Decode the received message
        received_data = msg.payload.decode("utf-8")
        print(f"Received data: {received_data}")

        # Attempt to parse the received data as JSON
        data = json.loads(received_data)

        # Extract the device ID from the received data
        device_id = data.get("DEVICE_ID")
        if device_id is not None:
            # Find the corresponding device name
            device_name = device_id

            if device_name in thingsboard_clients:
                payload = json.dumps(data)
                thingsboard_clients[device_name].publish(THINGSBOARD_TOPIC, payload, qos=1)
                print(f"Published data to ThingsBoard for {device_name}: {data}")
            else:
                print(f"No matching device found for DEVICE_ID: {device_id}")

    except Exception as e:
        print(f"Error processing message: {e}")

def on_disconnect(client, userdata, rc):
    """Callback for when the client disconnects from the broker."""
    print(f"Disconnected from broker with result code: {rc}")
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        client.reconnect()

def main():
    global thingsboard_clients

    # Set up the Mosquitto client
    mosquitto_client = mqtt.Client()
    mosquitto_client.on_message = on_message

    # Connect to the Mosquitto broker and subscribe to the topic
    mosquitto_client.connect(MOSQUITTO_BROKER, MOSQUITTO_PORT, 60)
    mosquitto_client.subscribe(MOSQUITTO_TOPIC, qos=1)

    # Set up the ThingsBoard clients for each device
    for device, token in devices.items():
        if token:
            client = mqtt.Client()
            client.username_pw_set(token)
            client.on_disconnect = on_disconnect  # Handle disconnections
            client.connect(THINGSBOARD_BROKER, THINGSBOARD_PORT, 60)
            thingsboard_clients[device] = client

    # Start the network loop for the Mosquitto client
    mosquitto_client.loop_start()

    # Start the network loop for each ThingsBoard client
    for client in thingsboard_clients.values():
        client.loop_start()

    print("Listening for messages...")

    try:
        # Keep the script running
        while True:
            pass
    except KeyboardInterrupt:
        print("Script interrupted. Disconnecting clients...")
        mosquitto_client.loop_stop()
        mosquitto_client.disconnect()
        for client in thingsboard_clients.values():
            client.loop_stop()
            client.disconnect()

if __name__ == "__main__":
    main()