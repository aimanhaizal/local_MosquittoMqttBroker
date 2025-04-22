import paho.mqtt.client as mqtt
import time
import json

broker = "10.1.43.8"
port = 1884
topic = "test/topic"
num_publishers = 10
messages_per_second = 3
duration = 30
total_messages_expected = num_publishers * messages_per_second * duration  # Total expected messages
received_messages = 0
latencies = []  # To track latencies
message_timestamps = {}  # To store the timestamp of each message for latency calculation

def on_connect(client, userdata, flags, rc):
    print(f"Subscriber connected with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global received_messages
    received_messages += 1

    try:
        payload = json.loads(msg.payload.decode())
        publish_time = float(payload["timestamp"])  # Now properly reads it
        latency = time.time() - publish_time
        latencies.append(latency)
        print(f"Received: {payload} | Latency: {latency:.4f}s")
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"Failed to process message: {msg.payload.decode()} | Error: {e}")



# Start subscriber clients
def start_subscriber():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.loop_start()

# Start 3 subscriber threads
for _ in range(3):
    start_subscriber()

# Wait for the message stream to end (30 seconds or until no more messages are received)
time.sleep(duration + 10)  # Allow some time after publishers finish

# Calculate throughput, latency, and message loss
total_latency = sum(latencies)
average_latency = total_latency / len(latencies) if latencies else 0
throughput = received_messages / duration  # Messages received per second
message_loss = total_messages_expected - received_messages  # Messages that were not received

print(f"Total messages expected: {total_messages_expected}")
print(f"Total messages received: {received_messages}")
print(f"Message loss: {message_loss}")
print(f"Throughput: {throughput:.2f} messages/sec")
print(f"Average latency: {average_latency:.4f} seconds")
