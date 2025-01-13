import paho.mqtt.client as mqtt
import time
import threading

broker = "localhost"  # MQTT broker address
port = 1883  # MQTT port
topic = "test/topic"
messages_per_second = 3  # 3 messages per second
num_publishers = 10
duration = 30  # Time to send messages in seconds

# Time tracking for simulation
start_time = time.time()

# This will hold the data to calculate throughput, latency, and message loss
message_count = [0] * num_publishers

def on_connect(client, userdata, flags, rc):
    print(f"Publisher connected with result code {rc}")
    
def publish_messages(publisher_id):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker, port, 60)
    client.loop_start()

    while time.time() - start_time < duration:
        payload = f"Publisher {publisher_id}: Message {message_count[publisher_id]}"
        client.publish(topic, payload)
        message_count[publisher_id] += 1
        time.sleep(1 / messages_per_second)  # Send 3 messages per second

    client.loop_stop()
    print(f"Publisher {publisher_id} finished sending messages.")

# Start publisher threads
publisher_threads = []
for i in range(num_publishers):
    t = threading.Thread(target=publish_messages, args=(i,))
    publisher_threads.append(t)
    t.start()

# Wait for all publisher threads to finish
for t in publisher_threads:
    t.join()
