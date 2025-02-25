import os
import paho.mqtt.client as mqtt
import time
import random
import json  # Import the json module
from datetime import datetime
from inspect import getsourcefile
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# MQTT broker details
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
topic = os.getenv("MQTT_TOPIC")
data_file = os.getenv("DATA_FILE")

FRAME_COUNTER = 0
print_counter = 0

# Define the directory containing AWS data
DIRECTORY = os.path.dirname(getsourcefile(lambda: 0))
os.chdir(DIRECTORY)
AWS_DATA_DIR = os.path.join(DIRECTORY, "AWS_DATA")

# Define the payload generation function
def generate_payload(data_file):
    # Example placeholders for required values
    device = type('Device', (object,), {"device_id": 12, "user_id": 12})()  # Mock device object
    Timestamp = str(datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))

    # change to 1,3
    i = random.randint(0, 100)  # Random index for SORT_KEY

    file_list = os.listdir(AWS_DATA_DIR)
    file_list.sort()

    applianceDataFrame = pd.read_csv(os.path.join(AWS_DATA_DIR, data_file))
    totalApparent = applianceDataFrame.ApparentPower[FRAME_COUNTER]

    self = type('Self', (object,), {"ED_FLAG": True, "grad_value": 0.5})()  # Mock self object

    payload = {
        "DEVICE_ID": int(device.device_id),
        "SORT_KEY": f"{Timestamp}#{FRAME_COUNTER}",# change this to 1,3 for the sending 3 a second
        "CREATE_DATE": Timestamp,
        "CREATE_USER_ID": int(device.user_id),
        "UPDATE_DATE": Timestamp,
        "UPDATE_USER_ID": int(device.user_id),
        "APPARENT_POWER": totalApparent,
        "REACTIVE_POWER": int(applianceDataFrame.ReactivePower[FRAME_COUNTER]),  # Convert to native Python int
        "HARMONIC_DISTORTION_POWER": int(applianceDataFrame.HarmonicDistortionPower[FRAME_COUNTER]),  # Convert to native Python int
        "TOTAL_POWER_FACTOR": float(applianceDataFrame.TotalPowerFactor[FRAME_COUNTER]),  # Convert to native Python float
        "COEFFICIENT_REAL_3H": float(applianceDataFrame.CoefficientReal3H[FRAME_COUNTER]),  # Convert to native Python float
        "COEFFICIENT_REAL_5H": float(applianceDataFrame.CoefficientReal5H[FRAME_COUNTER]),  # Convert to native Python float
        "COEFFICIENT_REAL_7H": float(applianceDataFrame.CoefficientReal7H[FRAME_COUNTER]),  # Convert to native Python float
        "COEFFICIENT_REAL_9H": float(applianceDataFrame.CoefficientReal9H[FRAME_COUNTER]),  # Convert to native Python float
        "COEFFICIENT_REAL_70HZ": float(applianceDataFrame.CoefficientReal70Hz[FRAME_COUNTER]),  # Convert to native Python float
        "PHASE_SHIFT": float(applianceDataFrame.PhaseShift[FRAME_COUNTER]),  # Convert to native Python float
        "DETECTION": self.ED_FLAG,
        "GRADIENT": self.grad_value,
        "PRINT_COUNTER": print_counter
    }

    return payload 

# Set up MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker, port, 60)

# Start the loop to handle network traffic
client.loop_start()

try:
    while True:
        payload = generate_payload(data_file)  # Generate payload
        payload_str = json.dumps(payload)  # Serialize payload to JSON string
        print_counter = print_counter + 1
        print("\nprint_counter: ", print_counter)
        client.publish(topic, payload_str, qos=1)  # Publish the serialized payload
        print(f"Sent: {payload_str}")  # Print the sent payload (optional)

        FRAME_COUNTER += 1
        if FRAME_COUNTER == 400:
            FRAME_COUNTER = 0

        time.sleep(1)  # Wait for 1 second before sending the next message

except KeyboardInterrupt:
    print("Terminating the publisher.")

finally:
    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect from the broker
