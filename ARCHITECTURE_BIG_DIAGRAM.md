# Big Architecture Diagram (Core + Extensions)

This diagram shows how VeighNa runtime components and extension packages fit together.

```mermaid
flowchart LR

%% =========================
%% External layer
%% =========================
subgraph EXT[External Systems]
    EXCH["Exchanges / Brokers<br/>CTP, IB, Binance, XTP, ..."]
    HIST["Historical Data Providers<br/>RQData, XT, Polygon, ..."]
    USER[Operators / Quants]
end

%% =========================
%% Extension packages
%% =========================
subgraph GWEXT[Gateway Extensions vnpy_*]
    GWDOM[Domestic: ctp/mini/femas/sopt/xtp/tora/...]
    GWOVR[Overseas: ib/tap/da]
    GWSPL[Special: rqdata/rpcservice/xt]
end

subgraph APPEXT[App Extensions vnpy_*]
    APPCTA[CTA Strategy]
    APPSPREAD[Spread Trading]
    APPPORT[Portfolio Strategy]
    APPALGO[Algo Trading]
    APPOPT[Option Master]
    APPRISK[Risk Manager]
    APPREC[Data Recorder]
    APPDATA[Data Manager]
    APPSCRIPT[Script Trader]
    APPBACK[CTA Backtester]
    APPPAPER[Paper Account]
    APPPM[Portfolio Manager]
    APPWEB[Web Trader / RPC Service]
end

subgraph DBEXT[Database Extensions]
    DBSQL[sqlite/mysql/postgresql]
    DBNOSQL[mongodb/taos/dolphindb/...]
end

subgraph DFEXT[Datafeed Extensions]
    DFSET[xt/rqdata/tushare/tqsdk/wind/ifind/...]
end

subgraph COREAPI[Core API Extensions]
    RESTEXT[vnpy_rest]
    WSEXT[vnpy_websocket]
end

%% =========================
%% Core runtime
%% =========================
subgraph CORE[Core Runtime vnpy]
    subgraph APPLAYER[App Metadata Layer]
        BASEAPP["BaseApp<br/>app_name, engine_class, widget_name"]
    end

    subgraph MAIN[Main Orchestration]
        MAINENGINE["MainEngine<br/>add_gateway()<br/>add_app()<br/>send_order()/subscribe()"]
    end

    subgraph ENGINES[Built-in Engines]
        OMS["OmsEngine<br/>State Cache + OffsetConverter"]
        LOGE[LogEngine]
        EMAILE[EmailEngine]
    end

    subgraph EVENTSYS[Event System]
        EVQ[(Event Queue)]
        EVPROC["Event Thread<br/>FIFO Dispatch"]
        EVTIMER["Timer Thread<br/>EVENT_TIMER @ 1s"]
    end

    subgraph CONTRACTS[Canonical Contracts]
        BGGW[BaseGateway]
        BDB[BaseDatabase]
        BDF[BaseDatafeed]
        DM["Tick/Bar/Order/Trade/Position/Account/Contract/Quote<br/>+ Request Objects"]
    end
end

%% =========================
%% UI and integration
%% =========================
subgraph UI[UI + Integration]
    QT["Desktop Qt UI<br/>MainWindow + Monitors + App Widgets"]
    RPC["RPC/Web Service Layer<br/>REST/WS publish-consume pattern"]
end

%% =========================
%% Relationships
%% =========================
USER --> QT
USER --> RPC

EXCH --> GWDOM
EXCH --> GWOVR
EXCH --> GWSPL
HIST --> DFSET

RESTEXT --> GWDOM
WSEXT --> GWDOM
RESTEXT --> GWOVR
WSEXT --> GWOVR

GWDOM --> BGGW
GWOVR --> BGGW
GWSPL --> BGGW

BGGW --> MAINENGINE
MAINENGINE --> EVQ
EVQ --> EVPROC
EVTIMER --> EVQ

EVPROC --> OMS
EVPROC --> LOGE
EVPROC --> EMAILE
EVPROC --> APPEXT
EVPROC --> QT
EVPROC --> RPC

MAINENGINE --> OMS
MAINENGINE --> APPEXT
BASEAPP --> MAINENGINE

APPEXT --> MAINENGINE
APPEXT --> EVQ
APPEXT --> DM

APPREC --> BDB
APPDATA --> BDB
APPBACK --> BDB
APPCTA --> BDF
APPPORT --> BDF

DBSQL --> BDB
DBNOSQL --> BDB
DFSET --> BDF

BDB --> MAINENGINE
BDF --> MAINENGINE

DM --> BGGW
DM --> OMS
DM --> APPEXT
```

## How Components Fit Together

1. `MainEngine` is the runtime hub.
   It boots built-in engines, loads gateway/app extensions, and routes trading API calls.

2. Gateways are the external boundary.
   Each gateway extension implements `BaseGateway` and converts broker payloads into canonical objects/events.

3. `EventEngine` is the system backbone.
   Gateways and apps publish events; the event thread dispatches them to OMS, apps, UI, and integration services.

4. `OmsEngine` is the in-memory source of truth.
   It maintains latest market/account/order/trade state and active orders/quotes for the whole process.

5. App extensions implement trading behavior.
   CTA/Spread/Portfolio/Algo/Option/Risk/etc. consume events and place/cancel orders through `MainEngine`.

6. Persistence is pluggable.
   Database adapters implement `BaseDatabase`; datafeed adapters implement `BaseDatafeed`; apps consume these interfaces without hard coupling.

7. UI and service integrations are subscribers.
   Desktop Qt widgets and RPC/Web layers react to the same event stream, keeping views aligned with engine state.
