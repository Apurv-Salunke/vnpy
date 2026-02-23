# tiny-trader-engine: Implementation Checklist

This is the execution plan to build `tiny-trader-engine` from scratch into a production-grade headless trading kernel with extensions.

## Naming and Scope

- Product name: `tiny-trader-engine`
- Core pipeline: `data -> strategy -> portfolio_risk -> oms`
- Architecture style: kernel + pip-installable extensions

## Repository Skeleton (Target)

```text
tiny_trader_engine/
  kernel/
    events/
      envelope.py
      schemas.py
      codecs.py
    interfaces/
      data_service.py
      strategy.py
      sizer.py
      risk_rule.py
      oms.py
      execution_policy.py
      broker_adapter.py
      fee_tax.py
    runtime/
      process_bootstrap.py
      health.py
      lifecycle.py
    bus/
      stream.py
      producer.py
      consumer.py
    journal/
      writer.py
      replay.py
      snapshots.py
    registry/
      entrypoints.py
      compatibility.py
      capabilities.py
    contracts/
      test_data_service_contract.py
      test_oms_contract.py
      test_risk_contract.py
      test_execution_policy_contract.py
  services/
    data_service/main.py
    strategy_runtime/main.py
    portfolio_risk/main.py
    oms_execution/main.py
    control_plane/main.py
    reconciliation/main.py
  configs/
    local.yaml
    paper.yaml
    live.yaml
  scripts/
    run_local.sh
    run_paper.sh
    run_live.sh
```

## Phase 0: Foundation and Contracts

### Build Tasks
- Create event envelope and canonical event schemas.
- Define all kernel interfaces.
- Define plugin capability model and versioning rules.
- Implement plugin registry via Python entry points.

### Files to Implement
- `tiny_trader_engine/kernel/events/envelope.py`
- `tiny_trader_engine/kernel/events/schemas.py`
- `tiny_trader_engine/kernel/interfaces/*.py`
- `tiny_trader_engine/kernel/registry/entrypoints.py`
- `tiny_trader_engine/kernel/registry/compatibility.py`

### Acceptance Criteria
- Schema validation rejects malformed events.
- Plugin loader discovers configured plugins.
- Incompatible plugin versions fail startup.

### Tests
- Unit tests for schema and registry behavior.
- Contract tests for each interface with mock implementations.

## Phase 1: Bus and Journal

### Build Tasks
- Implement message bus adapter (Redis Streams baseline).
- Implement durable append-only journal writer.
- Implement replay by offset and by time window.
- Add idempotency key utilities.

### Files to Implement
- `tiny_trader_engine/kernel/bus/stream.py`
- `tiny_trader_engine/kernel/bus/producer.py`
- `tiny_trader_engine/kernel/bus/consumer.py`
- `tiny_trader_engine/kernel/journal/writer.py`
- `tiny_trader_engine/kernel/journal/replay.py`

### Acceptance Criteria
- All core events are persisted once.
- Replay reconstructs event sequence exactly.
- Duplicate command detection works by idempotency key.

### Tests
- Integration test with bus + journal roundtrip.
- Restart test: replay produces deterministic state.

## Phase 2: OMS Core

### Build Tasks
- Implement canonical order state machine.
- Implement command path (`OrderIntent -> broker action`).
- Implement callback normalization path.
- Add timeout/cancel/replace handling.

### Files to Implement
- `tiny_trader_engine/services/oms_execution/main.py`
- `tiny_trader_engine/kernel/interfaces/oms.py`
- `tiny_trader_engine/kernel/interfaces/broker_adapter.py`

### Acceptance Criteria
- Invalid state transitions are rejected and alerted.
- Partial fill and cancel flows are deterministic.
- OMS does not double-apply callbacks after restart.

### Tests
- Transition table tests.
- Broker callback dedupe tests.
- Chaos test: disconnect/reconnect continuity.

## Phase 3: PortfolioRisk Engine

### Build Tasks
- Implement per-strategy and global ledgers.
- Implement sizing policies.
- Implement risk gate rules and reasons.
- Implement accounting module (commission/taxes/net pnl).

### Files to Implement
- `tiny_trader_engine/services/portfolio_risk/main.py`
- `tiny_trader_engine/kernel/interfaces/sizer.py`
- `tiny_trader_engine/kernel/interfaces/risk_rule.py`
- `tiny_trader_engine/kernel/interfaces/fee_tax.py`

### Acceptance Criteria
- Final risk gate is mandatory before OMS submission.
- Ledgers update correctly for fill/partial/cancel/reject.
- PnL with fees/taxes is reproducible from journal replay.

### Tests
- Deterministic ledger test suite.
- Risk-block reason and code assertions.

## Phase 4: Data Service

### Build Tasks
- Implement ingest adapters and normalization.
- Implement instrument master.
- Implement query API for bars/ticks/snapshots.
- Implement data quality guards.

### Files to Implement
- `tiny_trader_engine/services/data_service/main.py`
- `tiny_trader_engine/kernel/interfaces/data_service.py`

### Acceptance Criteria
- Stale/crossed/invalid data is blocked or flagged.
- Query API serves required windows for strategies.
- Event publication latency and lag metrics are emitted.

### Tests
- Adapter normalization tests.
- Data quality guard tests.

## Phase 5: Strategy Runtime

### Build Tasks
- Implement strategy manager and worker orchestration.
- Implement strategy lifecycle controls.
- Emit `SignalIntent` only.

### Files to Implement
- `tiny_trader_engine/services/strategy_runtime/main.py`
- `tiny_trader_engine/kernel/interfaces/strategy.py`

### Acceptance Criteria
- Multiple strategy instances run with isolated state.
- Strategy crash does not crash OMS/PortfolioRisk.
- Restart resumes from snapshot + replay without duplicate intents.

### Tests
- Multi-strategy isolation tests.
- Crash/restart replay tests.

## Phase 6: Control Plane and Reconciliation

### Build Tasks
- Build authenticated control API/CLI.
- Add global/strategy/symbol kill switches.
- Implement reconciliation worker and mismatch policies.

### Files to Implement
- `tiny_trader_engine/services/control_plane/main.py`
- `tiny_trader_engine/services/reconciliation/main.py`

### Acceptance Criteria
- Drift detection triggers configured policy actions.
- Kill switch blocks new order flow immediately.
- All control actions are audit logged.

### Tests
- Reconciliation mismatch simulation tests.
- Kill switch E2E tests.

## Phase 7: Observability and SLOs

### Build Tasks
- Add structured logging and metrics.
- Add tracing correlation across services.
- Define alert thresholds and incident classes.

### Acceptance Criteria
- Order latency and queue lag dashboards available.
- P0/P1/P2 alert routes tested.
- Incident triage can trace any order by correlation ID.

### Tests
- Telemetry coverage tests.
- Synthetic alert tests.

## Extension System Requirements

- Every extension must declare:
  - interface version compatibility
  - capability flags
  - plugin identifier
- Every extension must pass contract tests.
- Kernel startup fails closed on invalid extension.

## Example Entry Point Registration

```toml
[project.entry-points."tiny_trader_engine.oms"]
live_oms_v1 = "tiny_trader_ext_live_oms.plugin:LiveOmsPlugin"

[project.entry-points."tiny_trader_engine.data_service"]
options_data_v1 = "tiny_trader_ext_options_data.plugin:OptionsDataPlugin"
```

## Deployment Progression

1. Local single-host: Redis + Postgres + process supervisor.
2. Paper-trading environment with broker sim adapters.
3. Limited capital live rollout with strict kill-switch policy.
4. Multi-host scaling only after reconciliation and replay hardening.

## Production Readiness Gate (Mandatory)

Release is production-ready only if all are true:
- No order bypasses final risk gate.
- OMS transition coverage >= 100% on defined transitions.
- Replay consistency tests pass.
- Reconciliation mismatch policy tested.
- Kill-switch and drain-mode tested.
- Extension compatibility checks enforced at startup.
