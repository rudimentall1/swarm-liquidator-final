#  Swarm Liquidator — Real-Time MEV Execution Market Simulator

##  Overview

Swarm Liquidator is a real-time execution market simulator that makes MEV dynamics observable and reveals how latency creates non-linear instability in transaction ordering under competition.

It transforms blockchain execution from a black-box process into a live, interactive and measurable market.

---

## Problem

Modern decentralized execution systems are opaque.

Transaction ordering, MEV competition, and latency effects are hidden inside block production and are not observable in real time.

 HEAD
## Demo
[Swarm Liquidator — Real Time MEV Execution Market Simulator](https://www.youtube.com/watch?v=qVC_Ut9EoSY)
=======
This makes it difficult to understand how execution behaves under congestion and competitive pressure.
 24db408 (Improve README for hackathon presentation)

---

##  Solution

We built a real-time execution market simulator where:

- Transactions enter a live mempool
- Distributed nodes compete using a scoring-based auction
- Execution ordering is determined under latency constraints
- A leader selection mechanism resolves final outcomes

This creates a visible and interactive execution environment.

---

##  What is implemented

- Real-time mempool transaction streaming
- Distributed node competition system
- Latency-aware scoring and execution
- Dynamic leader selection
- Live dashboard visualization
- MQTT-based event-driven architecture
- WebSocket real-time updates
- Narrative system for explaining execution state
- Stress mode (“Killer Mode”) for congestion simulation

---

##  Why this matters

Execution ordering is one of the most important but least visible components of decentralized systems.

Swarm Liquidator makes MEV dynamics observable in real time and shows that latency introduces non-linear instability in execution outcomes under competition.

This enables execution markets to be studied as dynamic systems rather than static models.

---

##  Architecture

- Transaction Generator → emits mempool events
- Node Layer → competing execution agents
- Leader Engine → selects execution outcome
- MQTT Broker → event distribution layer
- Dashboard Server → real-time visualization
- Frontend → interactive UI + narrative system

---

##  Tech Stack

- Python (core simulation)
- MQTT (event bus)
- FastAPI (backend)
- WebSockets (real-time updates)
- Vanilla JavaScript (frontend)

---

##  Demo

- Live dashboard with real-time bidding
- Latency-aware execution visualization
- Dynamic winner selection
- Stress testing via Killer Mode

---

##  Links

- GitHub: https://github.com/rudimentall1/swarm-liquidator-final
- Demo Video: https://youtu.be/qVC_Ut9EoSY
- Author: Rinat — https://dorahacks.io/hacker/Rinat

---

##  Key Insight

Latency does not just delay execution — it reshapes competitive outcomes in MEV markets.
