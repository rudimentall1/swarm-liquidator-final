import json
import paho.mqtt.client as mqtt

client = mqtt.Client()

mempool = {}

def on_connect(client, userdata, flags, rc):
    print("[MEMPOOL] active")
    client.subscribe("tx")

def on_message(client, userdata, message):
    tx = json.loads(message.payload)

    if tx.get("type") != "TX":
        return

    tx_id = tx["id"]

    # кладём в mempool
    mempool[tx_id] = tx

    print(f"[MEMPOOL] added TX {tx_id} (pool size={len(mempool)})")

    # рассылаем дальше всем nodes
    client.publish("mempool/update", json.dumps(mempool))

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
