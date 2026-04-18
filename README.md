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
git clone https://github.com/rudimentall1/swarm-liquidator-final
cd swarm-liquidator-final
pip install -r requirements.txt
mosquitto -v
# In 3 separate terminals:
python node.py agent_a
python node.py agent_b
python node.py agent_c
Demo Video
https://youtu.be/qVC_Ut9EoSY

Why This Wins
Real problem: Users lose real money on every liquidation

Working code: 3 agents, heartbeats, leader election

No central server: Pure P2P coordination

Verifiable: Ed25519 signatures prove fair order
