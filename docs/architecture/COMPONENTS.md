# Components Reference (Kernel + Extensions)

This document defines each component as a strict contract with clear boundaries.

For every component, read in this order:
1. `Responsibilities`
2. `Capabilities`
3. `Scope`
4. `Limitations`
5. `Extension Points`
6. `Current vnpy mapping` (where applicable)

## Global Rules

- Kernel contains contracts, schemas, lifecycle, plugin loading, compatibility checks.
- Concrete variants are pip-installable extensions.
- Backtest/paper/live implementations must share the same contracts.
- No component may bypass the canonical event model.

---

## Event Bus / Event Engine

### Responsibilities
- Accept canonical events from producers.
- Dispatch events to subscribers deterministically.
- Provide timer/heartbeat events.

### Capabilities
- FIFO processing semantics.
- Type-based subscription and fan-out.
- Backpressure monitoring hooks.

### Scope
- Transport and dispatch only.
- Not responsible for business logic or persistence.

### Limitations
- Single-loop dispatch can bottleneck under heavy handlers.
- Requires bounded queues + lag alarms to remain safe.

### Extension Points
- Bus backend implementation (in-memory, Redis Streams, NATS, Kafka).
- Codec/serialization implementations.

### Current vnpy mapping
- `vnpy/event/engine.py`
- `vnpy/trader/event.py`

---

## DataService (Data Handler)

### Responsibilities
- Ingest market/reference/alt data from adapters.
- Maintain instrument master and symbol metadata.
- Maintain query cache for recent/history windows.
- Publish normalized market/domain events.

### Capabilities
- Multi-source adapter support.
- Subscription and replay window APIs.
- Expose query API (`get_bars`, `get_tick`, `get_snapshot`, etc.).

### Scope
- Data correctness, normalization, and delivery.
- No strategy, portfolio, or order execution decisions.

### Limitations
- Dependent on source quality and source SLAs.
- Must guard against stale/invalid/crossed data.

### Extension Points
- Data adapters by market/use case (options, multi-asset, news, corp actions).
- Cache policies and storage backends.

### Current vnpy mapping
- `vnpy/trader/datafeed.py`
- Gateway market callbacks in `vnpy/trader/gateway.py` and `vnpy_*`
- Recorder/data manager modules (`vnpy_datarecorder`, `vnpy_datamanager`)

---

## StrategyRuntime

### Responsibilities
- Host and manage multiple strategy instances.
- Consume market/domain events.
- Emit `SignalIntent` (not broker orders).
- Manage strategy lifecycle and isolation.

### Capabilities
- Multi-strategy orchestration.
- Per-strategy config/state and controls (pause/stop/kill).
- Optional CPU offload for heavy computations.

### Scope
- Alpha/signal generation only.
- No direct fund/margin/risk ownership.

### Limitations
- Poor isolation can cause strategy interference.
- High CPU strategies require explicit worker isolation.

### Extension Points
- Strategy packs by asset class/use case.
- Signal translators (signal -> target position).

### Current vnpy mapping
- `vnpy_ctastrategy`, `vnpy_portfoliostrategy`, `vnpy_spreadtrading`, `vnpy_scripttrader`

---

## PortfolioRiskEngine

### Responsibilities
- Own funds, margin, holdings, and exposure state.
- Maintain per-strategy ledgers and global ledger.
- Perform sizing and policy/risk checks.
- Produce `OrderIntent` or `RiskBlocked`.
- Update accounting from execution events.

### Capabilities
- Limit frameworks (per day/per strategy/per symbol/global).
- Dynamic market-aware pre-trade checks.
- Position sizing policies.
- Net/gross/concentration controls.

### Scope
- Portfolio, risk, sizing, and accounting decision layer.
- Not responsible for broker protocol execution.

### Limitations
- Needs authoritative and timely fills/state from OMS.
- Risk quality is limited by data quality and rule completeness.

### Extension Points
- `ISizer` implementations.
- `IRiskRule` libraries.
- fee/tax models and jurisdiction-specific accounting rules.

### Current vnpy mapping
- Risk: `vnpy_riskmanager`
- Portfolio-like accounting: `vnpy_portfoliomanager`
- Strategy-local sizing patterns across strategy apps

---

## OMS / ExecutionEngine (Order Handler)

### Responsibilities
- Own canonical order state machine.
- Convert `OrderIntent` into broker actions.
- Execute with policy (plain, sliced, urgency profiles).
- Publish order lifecycle events.

### Capabilities
- Idempotent order command processing.
- Replace/cancel/timeout handling.
- Multi-policy execution (limit/TWAP/iceberg/etc.).

### Scope
- Execution correctness and order lifecycle management.
- No alpha generation and no portfolio policy ownership.

### Limitations
- Dependent on broker adapter correctness and API behavior.
- Must reconcile to avoid drift after disconnect/restart.

### Extension Points
- OMS variants (live, paper, backtest OMS).
- `IExecutionPolicy` implementations.
- routing policies by venue/symbol.

### Current vnpy mapping
- Main order routing in `vnpy/trader/engine.py` (`MainEngine.send_order`)
- Lifecycle cache in `OmsEngine`
- Algo execution modules: `vnpy_algotrading`, parts of spread/option engines

---

## BrokerAdapter Layer

### Responsibilities
- Translate canonical order/query commands to broker-specific APIs.
- Translate broker callbacks to canonical events.
- Maintain session, heartbeat, reconnect.

### Capabilities
- Broker-specific feature mapping.
- Callback dedupe and identifier normalization.
- Snapshot endpoints for reconciliation.

### Scope
- Protocol boundary only.
- No strategy/risk/business policy.

### Limitations
- Vendor API inconsistency and outages.
- Feature availability differs by broker.

### Extension Points
- Broker-specific adapters packaged independently.
- specialized adapters for options/multileg features.

### Current vnpy mapping
- `vnpy/trader/gateway.py`
- `vnpy_*` gateway packages (e.g., `vnpy_ib`, `vnpy_binance`)

---

## Accounting (Commission + Taxes + Net PnL)

### Responsibilities
- Compute transaction costs and taxes from fills.
- Maintain net/gross PnL views per strategy and globally.
- Emit ledger entries and accounting summaries.

### Capabilities
- Rule-driven cost modeling by product/venue/jurisdiction.
- Realized/unrealized PnL separation.
- Audit-friendly ledger output.

### Scope
- Post-trade accounting under portfolio ownership.

### Limitations
- Accuracy depends on complete fee/tax schedule configuration.
- Complex jurisdictional rules may require periodic updates.

### Extension Points
- `IFeeTaxModel` implementations by venue/jurisdiction.
- custom reporting modules.

### Current vnpy mapping
- Distributed across app modules; not a single centralized kernel component.

---

## Journal / Event Store

### Responsibilities
- Persist immutable event stream for audit/replay/recovery.
- Support sequence-based replay.

### Capabilities
- Append-only writes with ordering guarantees.
- Playback by offset/time/correlation.

### Scope
- Durability and replay substrate.

### Limitations
- Storage and throughput constraints if schema/events are excessive.
- Requires schema evolution governance.

### Extension Points
- journal backend implementations.
- snapshotting strategies.

### Current vnpy mapping
- Partial via JSON state files and DB modules; no unified canonical event journal.

---

## Reconciliation Service

### Responsibilities
- Compare internal vs broker orders/positions/funds.
- Classify and resolve drift or halt system safely.

### Capabilities
- periodic snapshot diff checks.
- auto-heal safe cases and escalate unsafe cases.

### Scope
- Operational consistency control.

### Limitations
- Broker snapshot APIs may be delayed/incomplete.
- Aggressive auto-heal policies can create side effects if not validated.

### Extension Points
- reconciliation policies per venue/asset class.
- mismatch severity policy plugins.

### Current vnpy mapping
- Usually user/engine specific logic; not a unified dedicated service.

---

## Control Plane (Headless Ops)

### Responsibilities
- Expose operational commands (start/stop/kill, limits updates, drain mode).
- Enforce authn/authz and audit for operator actions.

### Capabilities
- runtime control over strategy and risk lifecycle.
- global/symbol/strategy kill switches.

### Scope
- Operations and governance.

### Limitations
- If unsecured, becomes critical attack surface.
- needs strict policy and audit discipline.

### Extension Points
- CLI/API frontends.
- policy/authorization providers.

### Current vnpy mapping
- UI/manual control patterns exist; no single headless control-plane kernel by default.

---

## Observability Layer

### Responsibilities
- Provide logs, metrics, traces, and alerts across all components.
- Surface queue lag, reject spikes, mismatch alerts, and kill-switch events.

### Capabilities
- unified telemetry pipeline.
- component-level health and SLA indicators.

### Scope
- runtime visibility and incident response support.

### Limitations
- poor instrumentation leaves blind spots.
- high-cardinality metrics can become expensive.

### Extension Points
- metric exporters and alerting backends.
- trace correlation enrichers.

### Current vnpy mapping
- Logging exists via `LogEngine`; full distributed observability is typically external.

---

## Plugin Registry and Compatibility

### Responsibilities
- Discover installed extensions via entry points.
- Resolve plugin IDs from runtime config.
- Validate interface compatibility/capabilities before startup.
- Run contract tests or startup self-checks.

### Capabilities
- hot-swappable implementation selection at startup.
- fail-closed startup for incompatible plugins.

### Scope
- plugin wiring and admission control.

### Limitations
- depends on strict interface versioning discipline.
- weak CI gates can still allow low-quality extensions.

### Extension Points
- registry backends and policy engines.
- compatibility rule packs.

### Current vnpy mapping
- Extension ecosystem exists; full contract-based admission control is typically project-specific.

---

## Canonical Domain Model

### Responsibilities
- Define immutable contracts for events and domain objects.
- Standardize identifiers and causal tracing fields.

### Capabilities
- cross-component interoperability.
- replay and audit consistency.

### Scope
- schema and contract layer only.

### Limitations
- schema changes require migration/version strategy.
- insufficient fields force unsafe use of ad-hoc metadata.

### Extension Points
- schema version adapters.
- payload enrichers for optional domains.

### Current vnpy mapping
- `vnpy/trader/object.py` plus event constants in `vnpy/trader/event.py`

---

## Quick Trace Map

- Market data issue: `DataService` -> adapter -> bus lag -> strategy subscribers.
- Signal issue: `StrategyRuntime` instance state/config -> emitted `SignalIntent`.
- Risk block issue: `PortfolioRiskEngine` rule/sizer decision + market snapshot.
- Execution issue: `OMS` transition table + adapter callbacks + idempotency cache.
- Position mismatch: reconciliation snapshot diff -> ledger correction or halt.
