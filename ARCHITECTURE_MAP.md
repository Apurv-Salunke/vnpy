# Architecture Map (Onboarding + Design Review)

## 1) Runtime Core
- `MainEngine` is the composition root: starts `EventEngine`, registers built-in engines, and hosts gateways/apps.
- Key file: `vnpy/trader/engine.py` (`MainEngine`, `OmsEngine`, `LogEngine`, `EmailEngine`).
- Plugin model:
  - Gateway plugin: `main_engine.add_gateway(...)`
  - App plugin: `main_engine.add_app(...)` (loads app engine via `BaseApp.engine_class`)

## 2) Event System (Primary Backbone)
- `EventEngine` has:
  - one event-processing thread (FIFO queue consumption)
  - one timer thread emitting `EVENT_TIMER` at configured interval (default 1s)
- Event routing model:
  - producer -> `event_engine.put(Event(type, data))`
  - consumer handlers registered by event type (or general handlers)
- Core files:
  - `vnpy/event/engine.py`
  - `vnpy/trader/event.py`

### Event Flow (Market Data)
1. Gateway receives external tick/order/trade callback.
2. Gateway emits normalized event (`on_tick/on_order/on_trade`).
3. Event thread dispatches to OMS + strategy/risk/recorder/UI handlers.

## 3) Data Model Contract
- Normalized domain objects: `TickData`, `BarData`, `OrderData`, `TradeData`, `PositionData`, `AccountData`, `ContractData`, `QuoteData`.
- Request objects: `OrderRequest`, `CancelRequest`, `SubscribeRequest`, `HistoryRequest`.
- This abstraction decouples engines/apps from broker-specific payloads.
- Core file: `vnpy/trader/object.py`.

## 4) Gateway Layer (External Boundary)
- Contract defined by `BaseGateway` in `vnpy/trader/gateway.py`.
- Required responsibilities:
  - connect/subscribe/send/cancel/query operations
  - map external API payloads to vnpy objects
  - push standardized events
- Examples:
  - Binance: split REST + multiple WS clients (`vnpy_binance/vnpy_binance/linear_gateway.py`)
  - IB: wrapper over `EClient`/`EWrapper` (`vnpy_ib/vnpy_ib/ib_gateway.py`)

## 5) OMS + Order Lifecycle
- `OmsEngine` is the in-memory source of truth for latest state.
- Caches: ticks/orders/trades/positions/accounts/contracts/quotes + active orders/quotes.
- Offset conversion support per gateway via `OffsetConverter`.
- Core file: `vnpy/trader/engine.py` (`OmsEngine`).

### Order Flow
1. Strategy/app creates `OrderRequest`.
2. `MainEngine.send_order` routes to target gateway.
3. Gateway sends broker order and emits order/trade events.
4. OMS updates caches; strategy engines receive callbacks; UI updates monitors.

## 6) Strategy/App Engines
- CTA: `vnpy_ctastrategy/.../engine.py`
  - lifecycle (`init/start/stop`), event-driven callbacks, local stop orders
- Spread: `vnpy_spreadtrading/.../engine.py`
  - data/algo/strategy sub-engines
- Portfolio: `vnpy_portfoliostrategy/.../engine.py`
  - multi-symbol strategy execution
- Algo: `vnpy_algotrading/.../engine.py`
  - execution algos (TWAP/Iceberg/etc.), timer-driven updates
- OptionMaster: `vnpy_optionmaster/.../engine.py`
  - option portfolio/chain pricing + algo/risk subcomponents
- DataRecorder: `vnpy_datarecorder/.../engine.py`
  - asynchronous persistence of ticks/bars
- RiskManager: `vnpy_riskmanager/.../engine.py`
  - pre-trade interception by patching `main_engine.send_order`

## 7) UI + Integration Surfaces
- Desktop GUI: Qt main window builds monitors and app widgets dynamically.
  - file: `vnpy/trader/ui/mainwindow.py`
- RPC/web-style service path (in this repo): `vnpy_webtrader/vnpy_webtrader/engine.py`
  - publishes trading events through RPC server.

## 8) Persistence Boundaries
- Durable by default:
  - DB data via pluggable `BaseDatabase` adapters (`vnpy/trader/database.py` + `vnpy_sqlite/...` etc.)
  - some engine JSON state (e.g., CTA settings/data, spread settings/positions, option settings)
- Not uniformly durable across all engines:
  - algorithm execution runtime state is primarily in-memory unless app-specific persistence is added.

## 9) Extension Points (Where to Add New Capability)
1. New broker/data venue:
   - implement `BaseGateway`, map payloads to vnpy objects, emit events.
2. New strategy app:
   - add app package with `BaseApp` metadata + engine + (optional) UI widget.
3. New risk rule:
   - implement `RuleTemplate` in `vnpy_riskmanager/rules`.
4. New data backend:
   - implement database/datafeed adapter and load via global settings.
5. New execution logic:
   - add `AlgoTemplate` subclass and register in `AlgoEngine`.

## 10) Design Review Checklist (Fast)
- Does it preserve event ordering and non-blocking handlers?
- Are all broker payloads converted to canonical vnpy objects once?
- Is state ownership clear (OMS vs strategy-local vs persisted JSON/DB)?
- Are failure/restart semantics explicit (what is reconstructed vs lost)?
- Does the change introduce hidden coupling across engine/gateway/UI layers?
