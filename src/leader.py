import json
import time
import paho.mqtt.client as mqtt

from metrics import record, snapshot

client = mqtt.Client()

bids = {}

# -----------------------------
# SCORE FUNCTION (MEV + latency)
# -----------------------------
def compute_score(bid):
    base = bid["score"]
    latency_penalty = bid.get("latency", 0) * 10
    return base - latency_penalty


# -----------------------------
# MQTT CONNECT
# -----------------------------
def on_connect(client, userdata, flags, rc):
    print("[LEADER] MEV auction engine started")
    client.subscribe("mev/bid")


# -----------------------------
# MESSAGE HANDLER
# -----------------------------
def on_message(client, userdata, message):
    global bids

    data = json.loads(message.payload)

    tx = data["tx"]
    tx_id = tx["id"]

    node_id = data["node_id"]
    latency = data.get("latency", 0)

    # base bid from node
    base_score = data.get("bid", 0)

    final_score = compute_score({
        "score": base_score,
        "latency": latency
    })

    # store bid
    if tx_id not in bids:
        bids[tx_id] = []

    bids[tx_id].append({
        "node": node_id,
        "score": final_score,
        "latency": latency
    })

    # simulate block finalization delay
    time.sleep(0.2)

    # -----------------------------
    # FINALIZE BLOCK
    # -----------------------------
    best = max(bids[tx_id], key=lambda x: x["score"])

    # record metrics
    record(
        tx_id=tx_id,
        latency=best["latency"],
        score=best["score"]
    )

    print("\n================================")
    print("🚀 BLOCK FINALIZED (MEV SWARM)")
    print("================================")
    print("TX ID   :", tx_id)
    print("WINNER  :", best["node"])
    print("SCORE   :", round(best["score"], 4))
    print("LATENCY :", round(best["latency"], 4))
    print("================================\n")

    # occasional metrics snapshot
    stats = snapshot()
    if stats:
        print("[METRICS]", stats)

    # reset mempool for next block
    bids.clear()


# -----------------------------
# START
# -----------------------------
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
