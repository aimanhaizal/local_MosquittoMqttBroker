import os
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime
from inspect import getsourcefile
import pandas as pd
from dotenv import load_dotenv
import signal
import numpy as np

load_dotenv()

# MQTT broker details
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
topic = os.getenv("MQTT_TOPIC")

FRAME_COUNTER = 0
print_counter = 0

# Define the directory containing AWS data
DIRECTORY = os.path.dirname(getsourcefile(lambda: 0))
os.chdir(DIRECTORY)
AWS_DATA_DIR = os.path.join(DIRECTORY, "AWS_DATA")

# Device-specific ThingsBoard access tokens
devices = {
    "00Fridge": "yed_Fridge",
    "01CoffeeMaker": "yed_CoffeeMaker",
    "02Oven": "yed_Oven",
    "03InductionCooker": "yed_InductionCooker",
    "05AirConditionerPanasonic_CoffeeMaker": "yed_AirConditionerPanasonic",
    "06AirConditionerPanasonic_InductionCooker": "yed_Dishwasher",
    # Add more devices as needed
}

# Define the payload generation function
def generate_payload(data_file, device_id, detection=True):
    Timestamp = str(datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))

    applianceDataFrame = pd.read_csv(os.path.join(AWS_DATA_DIR, data_file))
    totalApparent = applianceDataFrame.ApparentPower[FRAME_COUNTER]

    # Calculate the real power using the apparent power and power factor
    realPower = totalApparent * applianceDataFrame.TotalPowerFactor[FRAME_COUNTER]
    efficiencyScore = applianceDataFrame.TotalPowerFactor[FRAME_COUNTER] * (1 - applianceDataFrame.HarmonicDistortionPower[FRAME_COUNTER])

    gradient = np.gradient(applianceDataFrame.ApparentPower)[FRAME_COUNTER]

    self = type('Self', (object,), {"ED_FLAG": detection, "grad_value": gradient})()  # Mock self object

    payload = {
        "DEVICE_ID": device_id,
        "SORT_KEY": f"{Timestamp}#{FRAME_COUNTER}",
        "CREATE_DATE": Timestamp,
        "CREATE_USER_ID": 12,  # Mock user ID
        "UPDATE_DATE": Timestamp,
        "UPDATE_USER_ID": 12,  # Mock user ID
        "APPARENT_POWER": totalApparent,
        "REACTIVE_POWER": int(applianceDataFrame.ReactivePower[FRAME_COUNTER]),
        "REAL_POWER": realPower,
        "EFFICIENCY_SCORE": efficiencyScore,
        "HARMONIC_DISTORTION_POWER": int(applianceDataFrame.HarmonicDistortionPower[FRAME_COUNTER]),
        "TOTAL_POWER_FACTOR": float(applianceDataFrame.TotalPowerFactor[FRAME_COUNTER]),
        "COEFFICIENT_REAL_3H": float(applianceDataFrame.CoefficientReal3H[FRAME_COUNTER]),
        "COEFFICIENT_REAL_5H": float(applianceDataFrame.CoefficientReal5H[FRAME_COUNTER]),
        "COEFFICIENT_REAL_7H": float(applianceDataFrame.CoefficientReal7H[FRAME_COUNTER]),
        "COEFFICIENT_REAL_9H": float(applianceDataFrame.CoefficientReal9H[FRAME_COUNTER]),
        "COEFFICIENT_REAL_70HZ": float(applianceDataFrame.CoefficientReal70Hz[FRAME_COUNTER]),
        "PHASE_SHIFT": float(applianceDataFrame.PhaseShift[FRAME_COUNTER]),
        "DETECTION": self.ED_FLAG,
        "GRADIENT": self.grad_value,
        "PRINT_COUNTER": print_counter
    }

    return payload

# Set up MQTT clients for each device
clients = {}
for device, token in devices.items():
    client = mqtt.Client()
    client.username_pw_set(token)
    client.connect(broker, port, 60)
    clients[device] = client

# Start the loop to handle network traffic for each client
for client in clients.values():
    client.loop_start()

def cleanup(*args):
    for device, client in clients.items():
        data_file = f"{device}.csv"
        if os.path.exists(os.path.join(AWS_DATA_DIR, data_file)):
            payload = generate_payload(data_file, device, detection=False)  # Generate payload with DETECTION = False
            payload_str = json.dumps(payload)  # Serialize payload to JSON string
            client.publish(topic, payload_str, qos=1)  # Publish the serialized payload
            print(f"Sent termination payload to {device}: {payload_str}")  # Print the sent payload (optional)

    for client in clients.values():
        client.loop_stop()  # Stop the loop
        client.disconnect()  # Disconnect from the broker
    print("Terminating the publisher.")
    exit(0)

# Register the cleanup function for SIGTERM, SIGHUP, and SIGINT
# signal.signal(signal.SIGTERM, cleanup)
# signal.signal(signal.SIGHUP, cleanup)
signal.signal(signal.SIGINT, cleanup)

try:
    while True:
        start_time = time.time()
        for device, token in devices.items():
            data_file = f"{device}.csv"
            if os.path.exists(os.path.join(AWS_DATA_DIR, data_file)):
                payload = generate_payload(data_file, device)  # Generate payload with device ID
                payload_str = json.dumps(payload)  # Serialize payload to JSON string
                print_counter += 1
                print(f"\nprint_counter: {print_counter}")
                clients[device].publish(topic, payload_str, qos=1)  # Publish the serialized payload
                print(f"Sent to {device}: {payload_str}")  # Print the sent payload (optional)

        FRAME_COUNTER += 1
        if FRAME_COUNTER == 400:
            FRAME_COUNTER = 0

        # Ensure the loop runs once per second
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cleanup()