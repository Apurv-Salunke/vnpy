# VeighNa Components Reference

This reference is optimized for onboarding and debugging: each component includes `Responsibilities`, `Capabilities`, `Scope`, and `Limitations`.

## Extension-First Rule

- Component interfaces are stable contracts.
- Concrete implementations should be shipped as pip-installable extensions.
- Kernel should not accumulate strategy/use-case specific variants.
- Backtest/paper/live variants should implement the same contracts and be selected by configuration.

## How To Read This System

### Main entry point
- Runtime bootstrap path:
  - script entry (for example `examples/veighna_trader/run.py`)
  - create `EventEngine`
  - create `MainEngine`
  - `MainEngine.init_engines()` loads `LogEngine`, `OmsEngine`, `EmailEngine`
  - add gateways/apps via `main_engine.add_gateway(...)` and `main_engine.add_app(...)`
  - start UI (`MainWindow`) or service layer

### Fast tracing workflow
1. Start from the action: market event, order placement, strategy callback, or UI update.
2. Follow event type in `vnpy/trader/event.py` (`eTick.`, `eOrder.`, `eTrade.`, ...).
3. Find who publishes it (usually gateway or app engine).
4. Find handlers registered in engines (`event_engine.register(...)`).
5. Check `OmsEngine` cache updates for current state.
6. Check app-engine specific maps (`orderid_strategy_map`, `symbol_strategy_map`, etc.).

---

## EventEngine (`vnpy/event/engine.py`)

### Responsibilities
- Own central event queue.
- Dispatch events to type-specific and general handlers.
- Emit timer heartbeat events (`EVENT_TIMER`).

### Capabilities
- FIFO event processing in dedicated event thread.
- Separate timer thread with configurable interval.
- Dynamic registration/unregistration of handlers.

### Scope
- In-process pub/sub only.
- Delivery and sequencing, not business logic.

### Limitations
- Single event-processing thread can bottleneck under heavy handlers.
- No persistence/replay built in.
- Handler exceptions must be managed by handler code.

---

## MainEngine (`vnpy/trader/engine.py`)

### Responsibilities
- Compose system runtime (gateways + engines + apps).
- Route trading operations (`send_order`, `cancel_order`, `subscribe`, `query_history`).
- Provide access façade to OMS cache query functions.

### Capabilities
- Dynamic plugin loading for gateways/apps.
- Centralized lifecycle management (`close()` for engines/gateways).
- Unified API surface used by UI and app engines.

### Scope
- Orchestration and routing.
- Not strategy logic and not broker protocol specifics.

### Limitations
- No cross-process orchestration by itself.
- Depends on correctly implemented gateway/app plugins.

---

## BaseGateway + Gateway Implementations (`vnpy/trader/gateway.py`, `vnpy_*`)

### Responsibilities
- Translate external broker/exchange APIs into canonical vnpy objects.
- Push normalized events (`on_tick`, `on_order`, `on_trade`, ...).
- Execute broker-specific order/cancel/subscribe/query calls.

### Capabilities
- Per-venue protocol mapping and session handling.
- Per-symbol and per-order specific event fan-out (`EVENT_TICK + vt_symbol`, etc.).
- Optional history querying if venue supports it.

### Scope
- External boundary adapter layer.
- Venue-specific concerns only.

### Limitations
- Feature coverage varies by gateway.
- Behavior and latency depend on vendor SDK/network.
- Reconnect/state recovery quality is gateway-specific.

---

## OmsEngine (`vnpy/trader/engine.py`)

### Responsibilities
- Maintain latest in-memory state for core trading entities.
- Track active orders/quotes.
- Update offset converters for exchange-specific position semantics.

### Capabilities
- Fast lookup APIs (`get_order`, `get_position`, `get_all_active_orders`, etc.).
- Unified cache refreshed by event stream.

### Scope
- Runtime state cache and query point.
- Not long-term storage or reporting warehouse.

### Limitations
- In-memory only; process restart clears cache.
- “Latest state” model, not full event history.

---

## LogEngine (`vnpy/trader/engine.py`)

### Responsibilities
- Consume log events and output structured logs.

### Capabilities
- Level-based logging and gateway/app source tagging.

### Scope
- Logging output only.

### Limitations
- Not a metrics/trace backend.

---

## EmailEngine (`vnpy/trader/engine.py`)

### Responsibilities
- Asynchronous email delivery for alerts/notifications.

### Capabilities
- Background queue + SMTP send.

### Scope
- Notification transport.

### Limitations
- Depends on SMTP config and availability.
- Best-effort; no guaranteed delivery semantics.

---

## BaseApp + App Engines (`vnpy/trader/app.py`, `vnpy_*`)

### Responsibilities
- Package feature modules as plugin units (metadata + engine + optional UI widget).
- Implement domain logic (CTA, spread, portfolio, algo, options, risk, recorder, etc.).

### Capabilities
- Independent engines with dedicated event handlers.
- Reusable app loading via `main_engine.add_app(...)`.

### Scope
- Domain-specific behavior on top of core engine/event model.

### Limitations
- State persistence is uneven across apps.
- App interactions can become coupled through shared events if not designed carefully.

### Extension Guidance
- Keep app engine interfaces in kernel.
- Move specialized app engines to extension packages.
- Load by plugin ID and capability, not by hardcoded imports.

---

## RiskEngine (`vnpy_riskmanager/vnpy_riskmanager/engine.py`)

### Responsibilities
- Enforce pre-trade rules before order submission.

### Capabilities
- Rule plugin loading.
- Intercepts order path by patching `main_engine.send_order`.

### Scope
- Front-end risk gate, rule evaluation.

### Limitations
- Relies on in-process interception.
- Does not replace exchange/broker-side risk controls.

---

## RecorderEngine (`vnpy_datarecorder/vnpy_datarecorder/engine.py`)

### Responsibilities
- Record tick/bar/spread data into database asynchronously.

### Capabilities
- Buffered writes via background queue.
- Tick-to-bar aggregation support.

### Scope
- Market data capture pipeline.

### Limitations
- Backpressure and data loss risks if source rate exceeds processing/storage capacity.

---

## Datafeed Layer (`vnpy/trader/datafeed.py`, `vnpy_* datafeed adapters`)

### Responsibilities
- Provide standardized historical data query interface.

### Capabilities
- Pluggable provider adapters selected via settings.

### Scope
- Historical data retrieval only.

### Limitations
- Availability/schema/granularity vary by provider.
- Misconfiguration silently falls back to base no-op behavior.

### Extension Guidance
- Provider-specific logic must stay in provider extensions.
- Kernel should only enforce the datafeed interface and compatibility checks.

---

## Database Layer (`vnpy/trader/database.py`, `vnpy_* database adapters`)

### Responsibilities
- Persist/load bar and tick data through unified interface.

### Capabilities
- Pluggable database backends (sqlite/mysql/postgresql/mongodb/etc.).
- Timezone normalization support.

### Scope
- Time-series persistence abstraction.

### Limitations
- Performance and consistency depend on adapter/backend.
- No universal transactional model across all adapters.

### Extension Guidance
- Database adapters should be independent extension packages.
- Kernel should validate declared capabilities (for example, bulk write support) before startup.

---

## UI Layer (`vnpy/trader/ui/mainwindow.py`)

### Responsibilities
- Render trading workstation UI.
- Load app widgets dynamically from app metadata.

### Capabilities
- Monitor components for ticks/orders/trades/positions/accounts/logs.
- App menu and dockable widget framework.

### Scope
- Desktop interaction layer.

### Limitations
- Qt main-thread constraints for UI updates.
- Visualization only; core correctness remains in engines/gateways.

---

## RPC/Web Integration (`vnpy_webtrader/vnpy_webtrader/engine.py`, `vnpy_rpcservice/*`)

### Responsibilities
- Expose core trading functions over RPC/web channels.
- Publish selected events for remote consumers.

### Capabilities
- Remote command and event distribution patterns.

### Scope
- Integration boundary for multi-process/remote clients.

### Limitations
- Security, auth, and deployment hardening are environment responsibilities.
- Network partition/failure handling is integration-dependent.

---

## Plugin Registry and Compatibility (Cross-Cutting)

### Responsibilities
- Discover installed extensions via entry points.
- Resolve plugin IDs from runtime config.
- Validate kernel-interface compatibility before start.
- Enforce capability requirements for selected runtime profile.

### Capabilities
- Hot-swappable implementation selection at startup.
- Contract-test execution for extension acceptance.

### Scope
- Boot-time validation and plugin wiring only.

### Limitations
- Requires disciplined semantic versioning for interfaces.
- Poor extension hygiene can still degrade runtime quality without strict CI gates.

---

## Data Model Contract (`vnpy/trader/object.py`)

### Responsibilities
- Define canonical objects used across gateways, engines, apps, and UI.

### Capabilities
- Uniform field semantics (`vt_symbol`, `vt_orderid`, etc.).
- Request-to-data conversion helpers (`create_order_data`, `create_cancel_request`).

### Scope
- Shared domain schema and identifiers.

### Limitations
- Canonical model may not expose every exchange-specific nuance directly.
- Extensions may need `extra` metadata for venue-specific fields.
