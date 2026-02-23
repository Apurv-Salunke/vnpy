# Angel One gateway skeleton for VeighNa

This package contains a development skeleton for integrating Angel One SmartAPI
with VeighNa (`vn.py`).

## Scope of this skeleton

- Gateway scaffold (`AngelOneGateway`) with all required `BaseGateway` methods.
- Settings model for API credentials and connection configuration.
- Symbol/token mapper scaffold for instrument master handling.
- External paper-executor adapter interface scaffold.
- Run script wiring:
  - `AngelOneGateway`
  - `PaperAccountApp`
  - `DataManagerApp`

No live API calls are implemented yet. All network-facing methods contain TODO
markers.

## Install

```bash
uv pip install -e ./vnpy_angelone --system
```

## Quick start

```bash
python vnpy_angelone/script/run.py
```

Then in Trader UI:

1. Connect `ANGELONE`.
2. Subscribe symbols.
3. Use `PaperAccount` for local simulated execution.

## Implementation TODO checklist

1. SmartAPI session auth (api key, client code, pin/password, TOTP).
2. Instrument master download + token-to-symbol mapping.
3. WebSocket market data callbacks -> `TickData`.
4. Optional account/position pull and push.
5. Optional external paper broker adapter implementation in `paper_executor.py`.
