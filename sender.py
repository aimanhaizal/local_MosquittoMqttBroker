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


import paho.mqtt.client as mqtt
import time
import random
import string
import json  # Import the json module
from datetime import datetime

# MQTT broker details
broker = "10.1.43.8"
port = 1884
topic = "test/topic"

# Define the payload generation function
def generate_payload():
    # Example placeholders for required values
    device = type('Device', (object,), {"device_id": 12345, "user_id": 67890})()  # Mock device object
    Timestamp = str(datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))
    i = random.randint(0, 100)  # Random index for SORT_KEY
    totalApparent = random.uniform(0, 100)  # Random total apparent power
    FRAME_COUNTER = random.randint(0, 10)  # Random frame counter
    applianceDataFrame = type('ApplianceDataFrame', (object,), {
        "ReactivePower": [random.uniform(0, 10) for _ in range(11)],
        "HarmonicDistortionPower": [random.uniform(0, 10) for _ in range(11)],
        "TotalPowerFactor": [random.uniform(0, 1) for _ in range(11)],
        "CoefficientReal3H": [random.uniform(0, 1) for _ in range(11)],
        "CoefficientReal5H": [random.uniform(0, 1) for _ in range(11)],
        "CoefficientReal7H": [random.uniform(0, 1) for _ in range(11)],
        "CoefficientReal9H": [random.uniform(0, 1) for _ in range(11)],
        "CoefficientReal70Hz": [random.uniform(0, 1) for _ in range(11)],
        "PhaseShift": [random.uniform(0, 180) for _ in range(11)],
    })()  # Mock applianceDataFrame object
    self = type('Self', (object,), {"ED_FLAG": True, "grad_value": 0.5})()  # Mock self object
    print_counter = random.randint(1, 100)  # Random print counter

    payload = {
        "DEVICE_ID": int(device.device_id),
        "SORT_KEY": f"{Timestamp}#{i}",
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
        client.publish(topic, payload_str, qos=1)  # Publish the serialized payload
        print(f"Sent: {payload_str}")  # Print the sent payload (optional)
        time.sleep(1)  # Wait for 1 second before sending the next message

except KeyboardInterrupt:
    print("Terminating the publisher.")

finally:
    client.loop_stop()  # Stop the loop
    client.disconnect()  # Disconnect from the broker
