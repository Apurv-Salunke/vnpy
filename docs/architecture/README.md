# tiny-trader-engine Architecture Docs

This folder is the **source of truth** for TT architecture.

## Document Order (Read in Sequence)

1. `TARGET_HEADLESS_ARCHITECTURE.md`
- Product-level architecture and component boundaries.
- Defines kernel vs extensions and canonical flow.

2. `COMPONENTS.md`
- Contract-level component cards.
- Responsibilities, capabilities, scope, limitations, extension points.

3. `PYTHON_RUNTIME_EXECUTION_MODEL.md`
- Runtime execution details in Python.
- Process model, queues, threading, replay, reconciliation, operations.

4. `TINY_TRADER_ENGINE_IMPLEMENTATION_CHECKLIST.md`
- Build plan with phases, files, acceptance criteria, and tests.

## Naming Conventions

- Product name: `tiny-trader-engine` (TT)
- Python package root: `tiny_trader_engine`
- Plugin entry-point namespace: `tiny_trader_engine.*`
- Core service names:
  - `market_data`
  - `strategy_engine`
  - `portfolio_engine` (master: sizing/risk/ledger/accounting)
  - `execution_engine` (OMS)
  - `broker_gateway`
  - `control_plane`
  - `reconciliation_engine`
  - `event_log`

## Policy

- Keep kernel small: contracts, schemas, lifecycle, registry, compatibility.
- Put use-case variants in pip-installable extensions.
- Backtest/paper/live must implement the same contracts.
