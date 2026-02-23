# BANKNIFTY ATM Option Strategy Design (EMA Crossover + VWAP)

## 1) Strategy Goal
Design an intraday options strategy for BANKNIFTY that:
- selects **ATM option contracts** (CE/PE),
- enters on **EMA crossover + VWAP confirmation**,
- exits with **2% target** or **1% stop-loss**,
- risks at most **5% of account capital per trade**.

This design assumes single-leg long options (buy CE for bullish signal, buy PE for bearish signal).

## 2) Recommended Engine Choice
Use **CTA Strategy Engine** (`vnpy_ctastrategy`) for this use case.
- It already provides event-driven callbacks, order routing, stop-order support, lifecycle control, and persistence.
- OptionMaster is useful for volatility/chain analytics, but this strategy can run cleanly in CTA.

## 3) Component Responsibility Map
- **Gateway (`BaseGateway` implementation)**: broker/exchange connectivity, option quote/order/trade events.
- **EventEngine**: central event bus (`EVENT_TICK`, `EVENT_ORDER`, `EVENT_TRADE`, `EVENT_TIMER`).
- **CtaEngine**: strategy lifecycle (`init/start/stop`), event dispatch to strategy.
- **Strategy Class (custom `CtaTemplate`)**:
  - ATM contract selection
  - signal generation (EMA + VWAP)
  - sizing (5% risk rule)
  - entry/exit management (2%/1%)
- **OmsEngine**: latest order/trade/account/contract cache.
- **RiskManager app (optional but recommended)**: hard pre-trade guardrails.
- **Database/DataRecorder**: historical/live data recording.

## 4) Contract Selection Logic (ATM)
1. Read BANKNIFTY underlying price (index feed or liquid futures proxy).
2. Compute ATM strike:
   - `atm_strike = round(underlying / strike_step) * strike_step`
   - `strike_step` configurable (typically 100 for BANKNIFTY).
3. Build target symbols for current expiry:
   - bullish side -> ATM **CE**
   - bearish side -> ATM **PE**
4. Resolve to `vt_symbol` from contract cache (`MainEngine.get_all_contracts`).
5. Subscribe the selected option contract market data.

## 5) Signal Logic
On bar close (e.g., 1-min bars):
- compute `ema_fast`, `ema_slow`, and `vwap`.
- **Bullish entry**: `ema_fast` crosses above `ema_slow` and price > VWAP -> buy ATM CE.
- **Bearish entry**: `ema_fast` crosses below `ema_slow` and price < VWAP -> buy ATM PE.
- Skip new entries if already in position.

## 6) Position Sizing and Risk (5% Capital)
Inputs:
- `capital = account.balance`
- `risk_budget = capital * 0.05`
- `entry_price = option_ltp`
- `stop_price = entry_price * 0.99`
- `lot_size = contract.size`

Risk per lot:
- `risk_per_lot = (entry_price - stop_price) * lot_size`
- here, `risk_per_lot ≈ entry_price * 0.01 * lot_size`

Lots to trade:
- `lots = floor(risk_budget / risk_per_lot)`
- `qty = lots * lot_size`
- if `lots < 1`, skip trade.

## 7) Exit Management
After entry:
- `target_price = entry_price * 1.02`
- `stop_price = entry_price * 0.99`
- exit if LTP >= target (book profit)
- exit if LTP <= stop (cut loss)
- force square-off near market close (time-based risk control)

## 8) Strategy State and Persistence
Persist via CTA engine JSON state:
- strategy parameters (EMA periods, risk %, strike step, max trades/day)
- runtime variables (active symbol, entry price, trade count, realized pnl)
Files in runtime `.vntrader`:
- `cta_strategy_setting.json`
- `cta_strategy_data.json`

## 9) Suggested Class Skeleton
`class BankNiftyAtmEmaVwapStrategy(CtaTemplate)`
- `on_init`: load history, warm indicators, preload contract map
- `on_tick`: update `BarGenerator`
- `on_bar`: evaluate signal, select ATM contract, size, send orders
- `on_order`/`on_trade`: maintain state, update entry and exits
- helper methods: `select_atm_contract()`, `calculate_position_size()`, `check_exit_rules()`

## 10) Validation Path
1. Backtest in CTA backtester with realistic costs/slippage.
2. Paper trade with same risk caps.
3. Enable RiskManager hard limits (max order count/size, kill switch).
4. Run live with monitoring + DataRecorder enabled.

## 11) Practical Notes
- Option spreads/slippage can violate 1% stop in fast markets; handle with limit/market fallback policy.
- Recompute ATM symbol when underlying moves materially or at configurable intervals.
- Weekly expiry behavior should be explicit (which expiry to trade and rollover timing).
