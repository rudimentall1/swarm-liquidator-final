import time

metrics = {
    "tps": [],
    "latency": [],
    "scores": []
}

def record_metric(latency, score):
    metrics["latency"].append(latency)
    metrics["scores"].append(score)
    metrics["tps"].append(time.time())

def snapshot():
    if not metrics["latency"]:
        return {}

    return {
        "avg_latency": sum(metrics["latency"]) / len(metrics["latency"]),
        "max_latency": max(metrics["latency"]),
        "avg_score": sum(metrics["scores"]) / len(metrics["scores"]),
        "tx_count": len(metrics["scores"])
    }
