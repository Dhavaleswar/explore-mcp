import json
import time
import random
from kafka import KafkaProducer

# 🏢 Connect to the 3-broker cluster
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("🚀 Cluster Weather Station started. Sending data...")

try:
    while True:
        data = {
            'station_id': 'station_01',
            'temperature': random.randint(15, 40)
        }
        
        # Send data to our topic
        producer.send('weather-updates', value=data)
        print(f"Sent: {data}")
        
        time.sleep(2)
except KeyboardInterrupt:
    print("Stopping Producer...")
finally:
    producer.close()
