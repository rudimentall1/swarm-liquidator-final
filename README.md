# Swarm Liquidator

P2P liquidation-coordination prototype focused on deterministic ordering, agent liveness, and cryptographic agreement.

## Problem

Liquidation execution can be affected by transaction-order competition and front-running dynamics. A coordinated agent swarm can instead agree on an execution order before submitting it.

## Solution

Three P2P agents discover one another, exchange heartbeats, elect a leader, agree on a liquidation order, and sign the resulting decision with Ed25519.

## Flow

```text
Peer Discovery
      |
Heartbeats / Liveness
      |
Leader Election
      |
Liquidation Ordering
      |
Ed25519 Signatures
      |
Execution
```

## Run

```bash
git clone https://github.com/rudimentall1/swarm-liquidator-final
cd swarm-liquidator-final
pip install -r requirements.txt
mosquitto -v
```

Start the three agents in separate terminals using the project commands.

## Status

Prototype / challenge implementation demonstrating P2P coordination and signed decision flow. Production DeFi integration and adversarial consensus handling remain future work.
