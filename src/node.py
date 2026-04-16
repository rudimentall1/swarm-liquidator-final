import json
import time
import random
import sys
import paho.mqtt.client as mqtt

node_id = sys.argv[1] if len(sys.argv) > 1 else "1"

client = mqtt.Client()

base_speed = random.uniform(0.05, 0.25)

def compute_bid(tx):
    return (
        tx["amount"] * tx["priority"]
        - tx["risk"] * 15
        + random.uniform(0, 5)
    )

def on_connect(client, userdata, flags, rc):
    print(f"[NODE {node_id}] connected")
    client.subscribe("mempool/update")

def on_message(client, userdata, message):
    pool = json.loads(message.payload)

    # node выбирает лучший TX из mempool
    best_tx = None
    best_bid = -999

    for tx_id, tx in pool.items():
        time.sleep(base_speed * 0.1)

        bid = compute_bid(tx)

        if bid > best_bid:
            best_bid = bid
            best_tx = tx

    if best_tx:
        latency = time.time() - best_tx["ts"]

        packet = {
            "tx": best_tx,
            "node_id": node_id,
            "bid": best_bid,
            "latency": latency
        }

        print(f"[NODE {node_id}] best_bid={round(best_bid,2)}")

        client.publish("mev/bid", json.dumps(packet))

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
