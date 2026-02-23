# Expected Trading Architecture

This document defines the expected execution architecture for strategy-driven trading.

## Core Principle

Risk validation should happen **after quantity is decided** and **immediately before order submission**, using current market conditions.

## High-Level Flow

```mermaid
flowchart LR
    E[Event Engine]

    DH[Data Handler]
    SH[Strategy Handler]
    PH[Portfolio Handler]
    OH[Order Handler]

    S1[Strategy-1]
    S2[Strategy-2]

    PS[Position Sizer]
    RM[Risk Manager\n(Final Pre-Trade Gate)]
    GW[Gateway / Broker]

    E --> DH
    E --> SH
    E --> PH
    E --> OH

    SH --> S1
    SH --> S2

    PH --> PS
    PS --> RM
    RM -->|Pass| OH
    RM -->|Block/Modify| PH

    OH --> GW
```

## Execution Sequence (Authoritative)

1. Strategy generates trade intent (symbol, direction, rationale).
2. Portfolio/position sizing determines target quantity.
3. Final pre-trade risk gate evaluates:
   - latest market conditions (spread, liquidity, volatility, slippage risk)
   - portfolio and account constraints
   - operational guards (rate limits, stale data, kill switch)
4. If risk passes, order is submitted to order handler/gateway.
5. If risk fails, order is blocked (or modified) and logged.

## Risk Layers

### 1) Pre-sizing constraints
Applied before or during sizing:
- max gross/net exposure
- symbol-level limits
- strategy-level budget/capital caps

### 2) Final pre-trade gate (mandatory)
Applied right before send:
- real-time market condition checks
- order validity checks
- dynamic risk controls under current conditions

## Responsibilities by Component

- `Event Engine`: asynchronous event distribution.
- `Data Handler`: normalized market/account/order event ingestion.
- `Strategy Handler`: routes events to strategy modules.
- `Portfolio Handler`: exposure and sizing orchestration.
- `Position Sizer`: computes executable quantity.
- `Risk Manager`: final decision gate before execution.
- `Order Handler`: order construction/submission/cancel flow.

## Design Intent

- Keep strategy logic modular.
- Centralize final execution safety at a single risk gate.
- Ensure no order reaches gateway without current-condition risk validation.
