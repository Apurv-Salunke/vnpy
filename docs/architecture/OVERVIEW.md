# VeighNa Architecture Overview

## Purpose

VeighNa is designed as an event-driven trading platform where broker-specific adapters, strategy engines, and UI/service layers remain loosely coupled through a common event bus and canonical data model.

---

## System Philosophy (Why It Is Designed This Way)

### 1. Boundary isolation
- **Why:** Broker APIs are heterogeneous and unstable.
- **Design choice:** Put all venue/protocol complexity in gateway extensions.
- **Effect:** Strategy and app code remain broker-agnostic.

### 2. Canonical domain model
- **Why:** Every component needs shared semantics for orders/trades/positions.
- **Design choice:** Standard objects in `vnpy/trader/object.py`.
- **Effect:** Engines/apps/UI can interoperate without per-broker parsing logic.

### 3. Event-driven decoupling
- **Why:** Market data and order updates are asynchronous and bursty.
- **Design choice:** Central `EventEngine` queue + handler registration.
- **Effect:** Producers and consumers evolve independently; features compose via events.

### 4. Deterministic core processing
- **Why:** Trading state transitions must be understandable and debuggable.
- **Design choice:** Single event-processing thread (FIFO).
- **Effect:** Predictable ordering, lower race-condition complexity, easier replay reasoning.

### 5. Plugin-first extensibility
- **Why:** Users need custom gateways, apps, rules, and storage backends.
- **Design choice:** `BaseGateway`, `BaseApp`, `BaseDatabase`, `BaseDatafeed` contracts.
- **Effect:** Extension packages can be added with minimal core changes.

### 6. Runtime state + selective durability
- **Why:** Low-latency operation and operational flexibility matter.
- **Design choice:** OMS is in-memory; app-level JSON/DB persistence where needed.
- **Effect:** Fast runtime operations with explicit persistence boundaries and recovery tradeoffs.

---

## Top-Level Architecture

```text
External Venues/Data
  -> Gateway Extensions (protocol translation)
  -> EventEngine (queue + dispatch)
  -> Engines (OMS/log/email + app engines)
  -> UI / RPC / Web integrations
  -> Database & Datafeed adapters (persistence/history)
```

---

## Main Entry Point

Typical runtime boot sequence:
1. Create `EventEngine`.
2. Create `MainEngine(event_engine)`.
3. `MainEngine` initializes built-in engines (`LogEngine`, `OmsEngine`, `EmailEngine`).
4. Add gateway/app plugins.
5. Start UI (`MainWindow`) or service layer.

Common script reference: `examples/veighna_trader/run.py`.

---

## How To Track Behavior (Practical)

### A. Track market data flow
1. Gateway callback receives vendor payload.
2. Gateway converts to `TickData` and calls `on_tick`.
3. `EventEngine` dispatches `EVENT_TICK`.
4. OMS/app engines/UI handlers process updates.

### B. Track order lifecycle
1. Strategy/app calls `MainEngine.send_order`.
2. (Optional) `RiskEngine` intercepts and validates.
3. Gateway sends broker order and emits `EVENT_ORDER`/`EVENT_TRADE`.
4. OMS updates cache; strategy callbacks and UI reflect new state.

### C. Track persistence boundaries
- Runtime latest state: OMS in memory.
- Historical market data: database adapters.
- Strategy/app settings/state: app-specific JSON files (component dependent).

---

## Core Tradeoffs

- **Pros:** modularity, extensibility, deterministic event flow, broker abstraction.
- **Cons:** single event thread throughput ceiling, uneven persistence across apps, adapter-quality dependency.

These tradeoffs prioritize correctness, maintainability, and extension velocity over maximal internal parallelism.
