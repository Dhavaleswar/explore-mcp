import json
import os
from kafka import KafkaConsumer

# 👥 Connect to the cluster as part of a Consumer Group
consumer = KafkaConsumer(
    'weather-updates',
    bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
    group_id='weather-monitoring-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest'
)

pid = os.getpid()
print(f"📥 Consumer Instance [PID: {pid}] started. Waiting for data...")

try:
    for message in consumer:
        weather_data = message.value
        temp = weather_data['temperature']
        print(f"[PID: {pid}] Received from Partition {message.partition}: {temp}°C")
        
        if temp > 35:
            print(f"🔥 ALERT! High temperature detected: {temp}°C!")
except KeyboardInterrupt:
    print(f"Stopping Consumer {pid}...")
finally:
    consumer.close()
