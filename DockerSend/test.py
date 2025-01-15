# import paho.mqtt.client as mqtt
# import time
# import random
# import string

# # MQTT broker details
# # broker = "172.17.0.1"
# broker = "10.1.43.8"
# port = 1884
# topic = "test/topic"

# # Generate a 60-byte payload (random string of 60 characters)
# def generate_payload():
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

# # Set up MQTT client
# client = mqtt.Client()

# # Connect to the broker
# client.connect(broker, port, 60)

# # Start the loop to handle network traffic
# client.loop_start()

# try:
#     while True:
#         payload = generate_payload()  # Generate 60-byte payload
#         client.publish(topic, payload, qos=1)  # Publish to the broker
#         print(f"Sent: {payload}")  # Print the sent payload (optional)
#         time.sleep(1)  # Wait for 1 second before sending the next message

# except KeyboardInterrupt:
#     print("Terminating the publisher.")

# finally:
#     client.loop_stop()  # Stop the loop
#     client.disconnect()  # Disconnect from the broker

# # change the code to take the data from the csv files with qos = 1
# #import the AWS_DATA

# import paho.mqtt.client as mqtt
# import time
# import threading

# broker = "10.1.43.8"
# port = 1884
# topic = "test/topic"
# messages_per_second = 3  # 3 messages per second
# num_publishers = 10
# duration = 30  # Time to send messages in seconds

# # Time tracking for simulation
# start_time = time.time()

# # This will hold the data to calculate throughput, latency, and message loss
# message_count = [0] * num_publishers

# def on_connect(client, userdata, flags, rc):
#     print(f"Publisher connected with result code {rc}")
    
# def publish_messages(publisher_id):
#     client = mqtt.Client()
#     client.on_connect = on_connect
#     client.connect(broker, port, 60)
#     client.loop_start()

#     while time.time() - start_time < duration:
#         payload = f"Publisher {publisher_id}: Message {message_count[publisher_id]}"
#         client.publish(topic, payload)
#         message_count[publisher_id] += 1
#         time.sleep(1 / messages_per_second)  # Send 3 messages per second

#     client.loop_stop()
#     print(f"Publisher {publisher_id} finished sending messages.")

# # Start publisher threads
# publisher_threads = []
# for i in range(num_publishers):
#     t = threading.Thread(target=publish_messages, args=(i,))
#     publisher_threads.append(t)
#     t.start()

# # Wait for all publisher threads to finish
# for t in publisher_threads:
#     t.join()

# #above code does not work    

# import os
# import pandas as pd
# from datetime import datetime

# # Define the directory containing AWS data
# AWS_DATA_DIR = "./AWS_DATA/"

# # Snippet to generate the payload
# def generate_payload():
#     file_list = os.listdir(AWS_DATA_DIR)
#     file_list.sort()
#     appliance_data_frame = pd.read_csv(os.path.join(AWS_DATA_DIR, file_list[0]))

#     frame_counter = 0  # Hardcoded frame counter
#     print_counter = 0
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     payload = {
#         "DEVICE_ID": 12345,  # Hardcoded device ID
#         "SORT_KEY": f"{timestamp}#1",
#         "CREATE_DATE": timestamp,
#         "CREATE_USER_ID": 67890,  # Hardcoded user ID
#         "UPDATE_DATE": timestamp,
#         "UPDATE_USER_ID": 67890,  # Hardcoded user ID
#         "APPARENT_POWER": appliance_data_frame.ApparentPower[frame_counter],
#         "REACTIVE_POWER": appliance_data_frame.ReactivePower[frame_counter],
#         "HARMONIC_DISTORTION_POWER": appliance_data_frame.HarmonicDistortionPower[frame_counter],
#         "TOTAL_POWER_FACTOR": appliance_data_frame.TotalPowerFactor[frame_counter],
#         "COEFFICIENT_REAL_3H": appliance_data_frame.CoefficientReal3H[frame_counter],
#         "COEFFICIENT_REAL_5H": appliance_data_frame.CoefficientReal5H[frame_counter],
#         "COEFFICIENT_REAL_7H": appliance_data_frame.CoefficientReal7H[frame_counter],
#         "COEFFICIENT_REAL_9H": appliance_data_frame.CoefficientReal9H[frame_counter],
#         "COEFFICIENT_REAL_70HZ": appliance_data_frame.CoefficientReal70Hz[frame_counter],
#         "PHASE_SHIFT": appliance_data_frame.PhaseShift[frame_counter],
#         "DETECTION": False,  # self.ED_FLAG
#         "GRADIENT": 0  # self.grad_value
#     }
#     print_counter = print_counter + 1
#     payload["PRINT_COUNTER"] = print_counter

##############
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
