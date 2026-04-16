import time
import json
import random
import paho.mqtt.client as mqtt
import sys

client = mqtt.Client()
client.connect("localhost", 1883, 60)

burst_mode = "--burst" in sys.argv

tx_id = 0

while True:
    rate = 0.1 if burst_mode else 1.0

    for _ in range(5 if burst_mode else 1):
        tx_id += 1

        tx = {
            "type": "TX",
            "id": tx_id,
            "amount": random.randint(1, 100),
            "priority": random.random(),
            "ts": time.time()
        }

        client.publish("tx", json.dumps(tx))
        print("[GEN]", tx)

    time.sleep(rate)
