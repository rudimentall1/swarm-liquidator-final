# Swarm Liquidator

## Idea

We eliminate MEV randomness by replacing transaction ordering with deterministic swarm consensus.

## How it works

- Nodes receive liquidation transactions
- Each node computes a score:
  
  score = amount + priority - risk

- All nodes independently produce the same result
- Leader selects the best transaction every block

## Why it's important

- Removes MEV ordering manipulation
- Deterministic execution
- Fair liquidation selection

## Demo
[Swarm Liquidator — Real Time MEV Execution Market Simulator](https://www.youtube.com/watch?v=qVC_Ut9EoSY)

Run:

```bash
./demo.sh
