import os
import paho.mqtt.client as mqtt
import time
import random
import json  # Import the json module
from datetime import datetime
from inspect import getsourcefile
import pandas as pd

# MQTT broker details
broker = "10.1.43.8"
port = 1884
topic = "test/topic"

FRAME_COUNTER = 0
print_counter = 0

# Define the directory containing AWS data
DIRECTORY = os.path.dirname(getsourcefile(lambda: 0))
os.chdir(DIRECTORY)
AWS_DATA_DIR = DIRECTORY+"/AWS_DATA/"

# Define the payload generation function
def generate_payload():
    # Example placeholders for required values
    device = type('Device', (object,), {"device_id": 12, "user_id": 12})()  # Mock device object
    Timestamp = str(datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))

    # change to 1,3
    i = random.randint(0, 100)  # Random index for SORT_KEY

    # change to counting up.
    # FRAME_COUNTER = 0  # Hardcoded frame counter

    file_list = os.listdir(AWS_DATA_DIR)
    file_list.sort()

    applianceDataFrame = pd.read_csv(os.path.join(AWS_DATA_DIR, file_list[0]))
    totalApparent = applianceDataFrame.ApparentPower[FRAME_COUNTER]

    self = type('Self', (object,), {"ED_FLAG": True, "grad_value": 0.5})()  # Mock self object
    # print_counter = random.randint(1, 100)  # Random print counter

    payload = {
        "DEVICE_ID": int(device.device_id),
        "SORT_KEY": f"{Timestamp}#{FRAME_COUNTER}",# change this to 1,3 for the sending 3 a second
        "CREATE_DATE": Timestamp,
        "CREATE_USER_ID": int(device.user_id),
        "UPDATE_DATE": Timestamp,
        "UPDATE_USER_ID": int(device.user_id),
        "APPARENT_POWER": totalApparent,
        "REACTIVE_POWER": applianceDataFrame.ReactivePower[FRAME_COUNTER],
        "HARMONIC_DISTORTION_POWER": applianceDataFrame.HarmonicDistortionPower[FRAME_COUNTER],
        "TOTAL_POWER_FACTOR": applianceDataFrame.TotalPowerFactor[FRAME_COUNTER],
        "COEFFICIENT_REAL_3H": applianceDataFrame.CoefficientReal3H[FRAME_COUNTER],
        "COEFFICIENT_REAL_5H": applianceDataFrame.CoefficientReal5H[FRAME_COUNTER],
        "COEFFICIENT_REAL_7H": applianceDataFrame.CoefficientReal7H[FRAME_COUNTER],
        "COEFFICIENT_REAL_9H": applianceDataFrame.CoefficientReal9H[FRAME_COUNTER],
        "COEFFICIENT_REAL_70HZ": applianceDataFrame.CoefficientReal70Hz[FRAME_COUNTER],
        "PHASE_SHIFT": applianceDataFrame.PhaseShift[FRAME_COUNTER],
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
        payload = generate_payload()  # Generate payload
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
