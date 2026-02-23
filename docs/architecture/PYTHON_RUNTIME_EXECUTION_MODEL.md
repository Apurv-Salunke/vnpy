# Python Runtime Execution Model (Headless, Production-Oriented)

This document defines how the target architecture runs in Python, including process topology, concurrency, event transport, lifecycle, and operational controls.

## 1. Scope and Intent

This is the execution model for the **target headless system**, not a description of vnpy internals.

Primary objectives:
- deterministic order path
- strict ownership boundaries
- fault isolation
- operational control without GUI
- replayable and auditable event flow

## 1.1 Extensibility Constraint

Do not place use-case variants directly in the kernel runtime packages.

Kernel packages should contain only:
- runtime orchestration and lifecycle
- interface definitions
- canonical event models
- plugin discovery/loading
- compatibility and contract-test harnesses

All domain/runtime variants must be extensions installed via pip.

## 2. Baseline Comparison vs vnpy-style In-Process Runtime

A vnpy-style setup commonly runs one process with a small number of threads (event thread, timer thread, gateway threads, optional DB threads). That is good for speed-to-start and single-process simplicity.

For this target system, prefer **multi-process actor-style runtime**:
- each core component runs independently
- communication through canonical events
- no shared mutable state across components

Why this model is preferred for production:
- process-level fault containment
- independent restarts and deployment of components
- clearer ownership for state and logic
- easier scaling and observability per subsystem

## 3. Process Topology (Single Host Baseline)

Recommended baseline processes:

1. `data_service`
- market and reference data ingestion
- instrument master + data cache
- data query API

2. `strategy_runtime`
- strategy lifecycle manager
- strategy instance orchestration
- emits `SignalIntent`

3. `portfolio_risk`
- sizing + risk gate
- per-strategy and global ledgers
- accounting (fees/taxes/net pnl)

4. `oms_execution`
- order state machine
- execution policy engine
- broker interaction adapter boundary

5. `control_plane`
- headless API/CLI for lifecycle and risk controls
- runtime config changes and kill switches

6. `reconciliation_worker` (separate process or inside `oms_execution` in phase 1)
- broker-vs-internal drift detection and auto-halt policies

7. `observability_agent` (optional separate process)
- metrics/traces forwarding, health aggregation

Implementation note:
- each process role may be provided by different extension implementations selected at startup.

## 4. Intra-Process Concurrency Model

Use `asyncio` loop per process plus bounded mailboxes.

Per process internals:
- one main asyncio event loop
- one inbound queue subscriber task
- one outbound publisher task
- N component tasks for internal handlers
- small thread islands only where SDK is blocking

Guideline:
- keep core business flow non-blocking in async tasks
- isolate blocking broker/vendor SDK calls in adapter threads
- isolate CPU-heavy strategy computations in process pools if needed

## 5. Threading and Worker Pattern by Process

## `data_service`
- 1 asyncio loop thread
- 0-2 adapter threads for blocking APIs
- optional background compaction/cache thread

## `strategy_runtime`
- 1 asyncio loop thread
- optional `ProcessPoolExecutor` for CPU-heavy signal generation
- no direct broker I/O threads

## `portfolio_risk`
- 1 asyncio loop thread
- optional accounting worker for batch recalculation

## `oms_execution`
- 1 asyncio loop thread
- 1-4 adapter threads for broker SDK/network callbacks
- timer task for order timeout/retry windows

## `control_plane`
- 1 asyncio loop thread
- web server (FastAPI/uvicorn or equivalent)

Expected total on single-host baseline: 6-8 processes, roughly 8-20 total threads depending on adapter model.

## 6. Event Transport and Bus

Phase 1 transport options (single host):
- Redis Streams (recommended baseline)
- NATS (if already available)
- ZeroMQ (if you need low overhead point-to-point)

Phase 2/3 transport options (multi-host + durability):
- NATS JetStream
- Kafka

Transport requirements:
- ordered per stream/partition
- consumer groups
- bounded lag monitoring
- replay by offset/sequence

Bus implementation is also extension-replaceable, but should honor the same bus contract expected by kernel processes.

## 7. Canonical Event Envelope

All events use a common envelope.

```json
{
  "event_id": "uuid-v7",
  "event_type": "SignalIntent",
  "ts": "2026-02-24T00:00:00.000Z",
  "source": "strategy_runtime",
  "strategy_id": "meanrev_01",
  "correlation_id": "corr-...",
  "causation_id": "event-id-that-triggered-this",
  "idempotency_key": "stable-key-per-command",
  "schema_version": "1.0",
  "payload": {}
}
```

Event types (minimum):
- `MarketTick`, `MarketBar`, `CorporateAction`, `NewsEvent`
- `SignalIntent`
- `OrderIntent`, `RiskBlocked`
- `OrderAccepted`, `OrderRejected`, `PartialFill`, `Fill`, `CancelAck`
- `PositionUpdate`, `LedgerEntry`, `RiskLimitBreach`
- `ControlCommand`, `SystemHeartbeat`, `ReconcileMismatch`

## 8. State Ownership Rules

Strict ownership (no ambiguity):
- `DataService`: instrument master, live cache, historical query cache
- `StrategyRuntime`: strategy internal state and config
- `PortfolioRisk`: exposure state, limits, ledgers, accounting state
- `OMS`: order state machine and broker interaction state

Read access across boundaries should occur through events or read APIs, not direct object references.

## 9. Order Path (Authoritative Runtime Flow)

1. `MarketTick/Bar` enters from `data_service`.
2. `strategy_runtime` emits `SignalIntent`.
3. `portfolio_risk` performs:
   - sizing
   - portfolio/strategy/global limits
   - final market-aware pre-trade checks
4. If passed, emits `OrderIntent`; else emits `RiskBlocked`.
5. `oms_execution`:
   - validates intent idempotency
   - generates execution plan (single child order or sliced plan)
   - routes broker commands via adapter
6. broker callbacks become canonical lifecycle events.
7. `portfolio_risk` updates ledgers/accounting from fills.
8. all major events append to durable journal.

## 10. OMS State Machine Model

Minimum order state model:
- `CREATED`
- `SENT`
- `ACKED`
- `PARTIALLY_FILLED`
- `FILLED` (terminal)
- `CANCEL_PENDING`
- `CANCELED` (terminal)
- `REJECTED` (terminal)
- `EXPIRED` (terminal)

Transition requirements:
- transition table enforced centrally
- invalid transitions are rejected and alerted
- every transition emits one event

## 11. Idempotency and Deduplication

Commands (`OrderIntent`, `CancelCommand`) must be idempotent.

Recommended mechanism:
- stable idempotency key by `(strategy_id, intent_id, child_index)`
- short-term dedupe cache in OMS
- persistent dedupe record in journal DB

Callback dedupe:
- dedupe by broker execution identifiers (`broker_order_id`, `fill_id`)
- maintain processed fill keys to prevent double counting

## 12. Journaling and Recovery

Durable event journal is mandatory.

Journal requirements:
- append-only writes
- monotonic sequence per stream
- schema versioning
- replay capability by range/time/strategy/order

Recovery sequence:
1. load last committed offsets per process
2. restore internal state snapshots
3. replay journal delta to current point
4. resume consumers
5. run reconciliation before opening new risk gate

## 13. Reconciliation Loop

Frequency:
- high-frequency for orders (e.g., 5-30s)
- medium-frequency for positions/funds (e.g., 30-120s)

Checks:
- open orders internal vs broker
- filled quantity internal vs broker
- position inventory internal vs broker
- account balances/margin internal vs broker

Actions:
- classify mismatch severity
- auto-heal if safe (sync state)
- halt relevant strategy/venue on severe drift
- emit `ReconcileMismatch` + alerts

## 14. Backpressure and Load Shedding

Every process queue must be bounded.

Controls:
- queue depth thresholds
- lag metrics and alerts
- drop policy only for non-critical informational events
- never drop order lifecycle events

If risk/OMS inbound queue exceeds threshold:
- block new `SignalIntent` admission
- raise degraded-mode alert

## 15. Control Plane and Runtime Operations

Control plane commands:
- process lifecycle: start/stop/restart/status
- strategy lifecycle: enable/disable/pause/resume
- risk controls: update limits, freeze symbol, global kill switch
- execution controls: cancel all, drain mode, read-only mode

All control actions must be:
- authenticated and authorized
- journaled as control events
- correlated to operator identity

## 16. Security and Secrets

Minimum requirements:
- broker keys in secret manager or encrypted vault
- no plaintext secrets in config files
- command API authn/authz
- network ACLs around broker/control endpoints

## 17. Observability Model

Minimum telemetry:
- event lag per process
- queue depth per process
- order transition latency (intent->sent->ack->fill)
- reject/cancel/error rates by broker/symbol/strategy
- reconciliation mismatch counters
- risk block rates and reasons

Alert classes:
- P0: OMS unavailable, reconciliation hard mismatch, kill switch triggered
- P1: queue saturation, reject spikes, adapter disconnects
- P2: elevated latency, intermittent data feed quality issues

## 18. Deployment Profiles

## Profile A: Single Host (starter production)
- all processes on one VM
- Redis Streams + Postgres journal
- local process supervisor (systemd/supervisord)

## Profile B: Split Host (mid-scale)
- data/strategy on host A
- risk/OMS on host B
- shared transport + journal store

## Profile C: Multi-Region (advanced)
- active/passive with failover policies
- strict leader election for OMS per account

## 19. Python Implementation Skeleton

Suggested package layout:

```text
runtime/
  processes/
    data_service.py
    strategy_runtime.py
    portfolio_risk.py
    oms_execution.py
    control_plane.py
    reconciliation_worker.py
  bus/
    consumer.py
    producer.py
    envelope.py
  events/
    schemas.py
    codecs.py
  state/
    snapshots.py
    stores.py
  journal/
    writer.py
    replay.py
  adapters/
    broker/
    data/
  plugins/
    strategy/
    risk/
    sizing/
    execution/
    fees/
  registry/
    entrypoints.py
    compatibility.py
    capabilities.py
  contracts/
    tests/
      test_data_service_contract.py
      test_oms_contract.py
      test_risk_rule_contract.py
      test_execution_policy_contract.py
```

Suggested extension repo/package layout:

```text
tradingext-<name>/
  pyproject.toml
  tradingext_<name>/
    plugin.py
    impl/
```

`pyproject.toml` entry point example:

```toml
[project.entry-points."tradingext.oms"]
live_oms_v1 = "tradingext_live_oms.plugin:LiveOmsPlugin"
```

## 19.1 Capability Negotiation at Startup

Kernel should perform startup handshake before enabling trading:
1. discover configured plugins by entry point
2. validate interface version compatibility
3. verify required capabilities for selected strategy/risk profile
4. run quick contract self-checks
5. only then open strategy intake and order flow

If any required plugin fails validation, startup must fail closed.

## 20. Startup and Shutdown Protocol

Startup order:
1. journal store + bus connectivity check
2. data_service
3. oms_execution + broker adapters
4. portfolio_risk
5. strategy_runtime
6. control_plane
7. reconciliation_worker

Shutdown order (graceful):
1. strategy intake off
2. OMS drain or cancel-all policy
3. persist snapshots + offsets
4. stop consumers/producers
5. terminate processes

## 21. Failure Scenarios and Expected Behavior

1. Broker disconnect
- OMS marks adapter degraded
- stops new intents or route-fails over if configured
- keeps retrying session with backoff

2. Strategy process crash
- strategy_runtime supervisor restarts process
- replay from journal
- no duplicate orders because OMS idempotency gate

3. Risk process lag
- queue threshold triggers degraded mode
- strategy_runtime throttles signal emission

4. Journal unavailable
- move to safe mode (no new order intents)
- continue read-only market processing

## 22. Phased Delivery Plan

## Phase 1 (minimum safe)
- process topology + canonical envelope
- OMS state machine + broker adapter contract
- basic portfolio risk gate
- journal append + replay by offset

## Phase 2 (operational hardening)
- reconciliation worker
- control plane + kill switches
- observability + alerting
- backpressure and degraded-mode controls

## Phase 3 (advanced execution)
- multi-policy execution framework
- advanced fee/tax models
- multi-host deployment and failover controls

## 23. Non-Negotiable Acceptance Criteria

A release is not production-ready unless all are true:
- no order can bypass final risk gate
- OMS transitions are validated and fully observable
- idempotency proven under restart/retry tests
- reconciliation mismatch policy tested in simulation
- journal replay restores consistent state
- kill switch is tested and documented
- configured extensions pass compatibility + contract checks
