import json
import asyncio
import queue
import time
import paho.mqtt.client as mqtt

from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

clients = set()
mqtt_queue = queue.Queue()

# -----------------------------
# STATE
# -----------------------------
latest_state = {
    "tx": None,
    "bids": [],
    "metrics": {},
    "narration": "system idle",
    "stage": "INIT"
}

killer_mode = False
demo_start_time = None


# -----------------------------
# PITCH ENGINE (CORE VALUE)
# -----------------------------
def pitch_narration(state, event=None):
    stage = state["stage"]

    if stage == "INIT":
        return "System initialized: waiting for mempool activity"

    if stage == "FLOW":
        return "Normal MEV auction flow: nodes competing for inclusion"

    if stage == "PRESSURE":
        return "Network congestion increasing: MEV competition intensifies"

    if stage == "KILLER":
        return "🔥 KILLER MODE: extreme congestion + high-frequency bidding race"

    return "running"


# -----------------------------
# BROADCAST
# -----------------------------
async def broadcast(payload):
    dead = []

    for ws in clients:
        try:
            await ws.send_text(json.dumps(payload))
        except:
            dead.append(ws)

    for d in dead:
        clients.discard(d)


# -----------------------------
# MQTT
# -----------------------------
def on_connect(client, userdata, flags, rc):
    print("[DASHBOARD] connected")
    client.subscribe("tx")
    client.subscribe("mev/bid")


def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    mqtt_queue.put((msg.topic, data))


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()


# -----------------------------
# METRICS
# -----------------------------
def update_metrics():
    bids = latest_state["bids"]
    if not bids:
        return

    lat = [b.get("latency", 0) for b in bids]
    sc = [b.get("score", 0) for b in bids]

    latest_state["metrics"] = {
        "avg_latency": sum(lat) / len(lat),
        "avg_score": sum(sc) / len(sc),
        "tx_count": len(bids)
    }


# -----------------------------
# DEMO STAGE ENGINE
# -----------------------------
def update_stage():
    global killer_mode

    bids = latest_state["bids"]

    if killer_mode:
        latest_state["stage"] = "KILLER"
    elif len(bids) > 20:
        latest_state["stage"] = "PRESSURE"
    elif len(bids) > 0:
        latest_state["stage"] = "FLOW"
    else:
        latest_state["stage"] = "INIT"


# -----------------------------
# WORKER LOOP
# -----------------------------
async def worker():
    global latest_state

    while True:
        while not mqtt_queue.empty():
            topic, data = mqtt_queue.get()

            if topic == "tx":
                latest_state["tx"] = data

            if topic == "mev/bid":
                latest_state["bids"].append(data)
                latest_state["bids"] = latest_state["bids"][-20:]

                update_metrics()
                update_stage()

                best = max(latest_state["bids"], key=lambda x: x["score"])

                latest_state["narration"] = pitch_narration(latest_state)

            await broadcast({
                "type": "update",
                "data": latest_state
            })

        await asyncio.sleep(0.05)


# -----------------------------
# KILLER MODE API
# -----------------------------
@app.post("/killer")
async def killer():
    global killer_mode, demo_start_time

    killer_mode = True
    demo_start_time = time.time()

    latest_state["stage"] = "KILLER"
    latest_state["narration"] = "🔥 KILLER MODE ACTIVATED"

    return {"status": "KILLER MODE ON"}


# -----------------------------
# DEMO RESET (IMPORTANT FOR PITCH)
# -----------------------------
@app.post("/reset")
async def reset():
    global killer_mode, demo_start_time

    killer_mode = False
    demo_start_time = None

    latest_state["bids"] = []
    latest_state["tx"] = None
    latest_state["metrics"] = {}
    latest_state["stage"] = "INIT"

    return {"status": "RESET OK"}


# -----------------------------
# STARTUP
# -----------------------------
@app.on_event("startup")
async def startup():
    asyncio.create_task(worker())
    print("[DASHBOARD] PITCH MODE READY")


# -----------------------------
# WS
# -----------------------------
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)

    try:
        while True:
            await asyncio.sleep(1)
    except:
        clients.discard(websocket)


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("dashboard_server:app", host="0.0.0.0", port=8000)
