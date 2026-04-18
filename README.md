# Swarm Liquidator — Stop MEV Theft on Liquidations

## Problem (Real Loss)
When you borrow crypto and your collateral drops, MEV bots front-run your liquidation. They see your transaction first, execute their own, and you lose money. This is not a bug. This is how current systems work.

## Solution (What We Fix)
We built a swarm of 3 P2P agents. They watch for risky positions, agree on a single fair liquidation order, and sign it. No front-running. No central server.

## How It Works (30 seconds)
1. Agent A, B, C discover each other (no setup needed)
2. Every 5 seconds they send heartbeats — swarm is alive
3. Every 30 seconds they elect a leader
4. Leader decides the liquidation order
5. All agents sign the decision (Ed25519)

## Run It Yourself
```bash
# Clone
git clone https://github.com/rudimentall1/swarm-liquidator-final
cd swarm-liquidator-final

# Install
pip install -r requirements.txt

# Terminal 1: Start broker
mosquitto -v

# Terminals 2, 3, 4: Run 3 agents
python node.py agent_a
python node.py agent_b
python node.py agent_c

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
