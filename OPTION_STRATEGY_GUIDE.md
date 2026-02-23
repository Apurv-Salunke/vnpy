# Dynamic Option Chain Strategy Guide

For strategies requiring **dynamic option chain support** (strike selection, expiry selection, multi-leg strategies based on signals).

---

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              Your Custom Option Strategy                         │
│  (extends Portfolio Strategy Template)                           │
├─────────────────────────────────────────────────────────────────┤
│  Signal Generation → Option Chain Analytics → Order Execution   │
│  - Underlying signal  - IV rank calculation  - Multi-leg orders │
│  - Volatility view    - Strike selection     - Risk management  │
│  - Expiry view        - Greeks targeting                          │
├─────────────────────────────────────────────────────────────────┤
│              vnpy_portfoliostrategy                              │
│  (Strategy lifecycle + Backtesting)                              │
├─────────────────────────────────────────────────────────────────┤
│              vnpy_optionmaster (Utilities)                       │
│  - OptionData, ChainData, PortfolioData                          │
│  - Black-Scholes, Black-76, Binomial pricing                     │
│  - Greeks calculation, IV calculation                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Why Not Pure OptionMaster?

| Feature | OptionMaster | Portfolio Strategy | Your Need |
|---------|--------------|-------------------|-----------|
| **Option chain mgmt** | ✅ Excellent | ⚠️ Manual | Need this |
| **Greeks/IV calc** | ✅ Excellent | ❌ None | Need this |
| **Strategy template** | ❌ Algo-based only | ✅ Flexible | Need this |
| **Backtesting** | ❌ Limited | ✅ Full support | Need this |
| **Dynamic selection** | ⚠️ Manual setup | ✅ Code-based | Need this |
| **Multi-leg** | ✅ Yes | ✅ Yes | Need this |

**Solution:** Use **Portfolio Strategy** as the base + **OptionMaster utilities** for pricing/Greeks.

---

## OptionMaster Key Classes to Reuse

### 1. OptionData (from vnpy_optionmaster/base.py)

```python
class OptionData(InstrumentData):
    """Option contract data with Greeks and IV"""
    
    # Contract features
    self.strike_price: float
    self.chain_index: str
    self.option_type: int  # 1=CALL, -1=PUT
    self.option_expiry: datetime
    self.days_to_expiry: int
    self.time_to_expiry: float
    
    # Pricing
    self.calculate_price: Callable      # Pricing model
    self.calculate_greeks: Callable     # Greeks calculation
    self.calculate_impv: Callable       # IV calculation
    
    # Implied volatility
    self.bid_impv: float
    self.ask_impv: float
    self.mid_impv: float
    self.pricing_impv: float
    
    # Greeks
    self.theo_delta: float
    self.theo_gamma: float
    self.theo_theta: float
    self.theo_vega: float
    
    # Position Greeks
    self.pos_delta: float
    self.pos_gamma: float
    self.pos_theta: float
    self.pos_vega: float
```

### 2. Pricing Models (from vnpy_optionmaster/pricing/)

```python
# Black-Scholes for European stock options
from vnpy_optionmaster.pricing import black_scholes

price, delta, gamma, theta, vega = black_scholes.calculate_greeks(
    underlying_price=18000,
    strike_price=18000,
    interest_rate=0.065,
    time_to_expiry=30/365,
    volatility=0.18,
    option_type=1  # CALL
)

# Black-76 for European futures options (like NIFTY/BANKNIFTY)
from vnpy_optionmaster.pricing import black_76

price, delta, gamma, theta, vega = black_76.calculate_greeks(
    underlying_price=47500,
    strike_price=47500,
    interest_rate=0.065,
    time_to_expiry=30/365,
    volatility=0.15,
    option_type=1  # CALL
)

# Implied volatility calculation
impv = black_76.calculate_impv(
    option_price=350,
    underlying_price=47500,
    strike_price=47500,
    interest_rate=0.065,
    time_to_expiry=30/365,
    option_type=1
)
```

---

## Strategy Example: Dynamic Straddle/Strangle

```python
# strategies/dynamic_option_strategy.py
from datetime import datetime, timedelta
from vnpy_portfoliostrategy import StrategyTemplate
from vnpy.trader.constant import Direction, Offset, OptionType
from vnpy.trader.object import BarData, TickData, ContractData
from vnpy.trader.utility import BarGenerator, ArrayManager

# Import OptionMaster pricing utilities
from vnpy_optionmaster.pricing import black_76
from vnpy_optionmaster.time import calculate_days_to_expiry, ANNUAL_DAYS


class DynamicOptionStrategy(StrategyTemplate):
    """
    Dynamic option strategy with automatic strike/expiry selection
    
    Features:
    - Selects expiry based on days-to-expiry target
    - Selects strikes based on moneyness (ATM/OTM/ITM)
    - Calculates IV and Greeks in real-time
    - Supports straddle, strangle, iron condor, etc.
    """
    
    author = "Your Name"
    
    # Strategy parameters
    strategy_type: str = "straddle"  # straddle, strangle, iron_condor
    expiry_days_target: int = 30     # Target days to expiry
    strike_distance: str = "ATM"     # ATM, OTM_1, OTM_2, ITM_1
    leg_ratio: int = 1               # Ratio for legs
    
    # Underlying parameters
    underlying_symbol: str = "BANKNIFTY.NSE"
    iv_rank_lookback: int = 252      # 1 year for IV rank
    
    # Risk management
    max_portfolio_delta: float = 0.3   # Max net delta
    stop_loss_pct: float = 0.5         # 50% stop loss
    take_profit_pct: float = 1.0       # 100% take profit
    
    parameters = [
        "strategy_type",
        "expiry_days_target",
        "strike_distance",
        "leg_ratio",
        "underlying_symbol",
        "max_portfolio_delta",
        "stop_loss_pct",
        "take_profit_pct"
    ]
    
    def __init__(self, cta_engine, strategy_name, vt_symbols, setting):
        super().__init__(cta_engine, strategy_name, vt_symbols, setting)
        
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager(size=252)  # For IV rank calculation
        
        # Option chain data
        self.option_chain = {}  # {vt_symbol: OptionData}
        self.selected_options = {}  # {leg_name: vt_symbol}
        
        # Position tracking
        self.entry_premium = {}  # {vt_symbol: entry_price}
        self.position_greeks = {
            "delta": 0,
            "gamma": 0,
            "theta": 0,
            "vega": 0
        }
        
        # State
        self.position_open = False
        self.legs_opened = set()
        
    def on_init(self):
        """Initialize strategy"""
        self.write_log("Strategy initialized")
        self.load_bar(60)  # Load 60 days for IV calculation
        
    def on_start(self):
        self.write_log("Strategy started")
        self.refresh_option_chain()
        
    def on_stop(self):
        self.write_log("Strategy stopped")
        self.close_all_positions()
        
    def on_bar(self, bar: BarData):
        """Main bar handler"""
        self.cancel_all()
        
        # Update underlying data
        self.am.update_bar(bar)
        
        # Refresh option chain periodically
        self.refresh_option_chain()
        
        # Check if we should open position
        if not self.position_open:
            self.check_entry_signal()
        else:
            self.check_exit_signal()
        
        self.put_event()
        
    def refresh_option_chain(self):
        """
        Refresh option chain data
        Select appropriate strikes and expiries
        """
        # Get all option contracts for underlying
        all_contracts = self.get_all_contracts()
        
        option_contracts = [
            c for c in all_contracts 
            if c.product == Product.OPTION 
            and self.underlying_symbol in c.option_underlying
        ]
        
        # Group by expiry
        expiry_groups = {}  # {expiry_date: [contracts]}
        for contract in option_contracts:
            expiry = contract.option_expiry
            if expiry not in expiry_groups:
                expiry_groups[expiry] = []
            expiry_groups[expiry].append(contract)
        
        # Select expiry closest to target
        selected_expiry = self.select_expiry(expiry_groups)
        if not selected_expiry:
            return
        
        # Get underlying price
        underlying_tick = self.get_tick(self.underlying_symbol)
        if not underlying_tick:
            return
        underlying_price = underlying_tick.last_price
        
        # Select strikes based on moneyness
        selected_strikes = self.select_strikes(
            expiry_groups[selected_expiry],
            underlying_price,
            self.strike_distance
        )
        
        # Build OptionData objects
        for contract in selected_strikes:
            option_data = self.create_option_data(contract, underlying_price)
            self.option_chain[contract.vt_symbol] = option_data
        
        # Select legs based on strategy type
        self.select_legs(selected_expiry, underlying_price)
        
        self.write_log(f"Option chain refreshed: {len(self.option_chain)} options")
        
    def select_expiry(self, expiry_groups: dict) -> datetime:
        """Select expiry closest to target days"""
        if not expiry_groups:
            return None
            
        today = datetime.now()
        best_expiry = None
        min_diff = float('inf')
        
        for expiry in expiry_groups.keys():
            days_diff = abs((expiry - today).days - self.expiry_days_target)
            if days_diff < min_diff:
                min_diff = days_diff
                best_expiry = expiry
        
        return best_expiry
        
    def select_strikes(
        self, 
        contracts: list[ContractData], 
        underlying_price: float,
        distance: str
    ) -> list[ContractData]:
        """Select strikes based on moneyness"""
        
        # Separate calls and puts
        calls = [c for c in contracts if c.option_type == OptionType.CALL]
        puts = [c for c in contracts if c.option_type == OptionType.PUT]
        
        # Sort by strike
        calls.sort(key=lambda x: x.option_strike)
        puts.sort(key=lambda x: x.option_strike)
        
        # Find ATM strike (closest to underlying price)
        atm_call = min(calls, key=lambda x: abs(x.option_strike - underlying_price))
        atm_strike = atm_call.option_strike
        
        selected = []
        
        if distance == "ATM":
            # Select ATM call and put
            atm_put = min(puts, key=lambda x: abs(x.option_strike - underlying_price))
            selected = [atm_call, atm_put]
            
        elif distance == "OTM_1":
            # Select 1 strike OTM
            call_otm = [c for c in calls if c.option_strike > atm_strike]
            put_otm = [p for p in puts if p.option_strike < atm_strike]
            if call_otm and put_otm:
                selected = [call_otm[0], put_otm[0]]
                
        elif distance == "OTM_2":
            # Select 2 strikes OTM
            call_otm = [c for c in calls if c.option_strike > atm_strike]
            put_otm = [p for p in puts if p.option_strike < atm_strike]
            if len(call_otm) > 1 and len(put_otm) > 1:
                selected = [call_otm[1], put_otm[1]]
        
        return selected
        
    def create_option_data(
        self, 
        contract: ContractData, 
        underlying_price: float
    ) -> 'OptionData':
        """Create OptionData with Greeks and IV"""
        
        # Calculate days to expiry
        days_to_expiry = calculate_days_to_expiry(contract.option_expiry)
        time_to_expiry = days_to_expiry / ANNUAL_DAYS
        
        # Get option tick
        tick = self.get_tick(contract.vt_symbol)
        if not tick:
            return None
            
        mid_price = (tick.bid_price_1 + tick.ask_price_1) / 2
        
        # Calculate IV
        impv = black_76.calculate_impv(
            option_price=mid_price,
            underlying_price=underlying_price,
            strike_price=contract.option_strike,
            interest_rate=0.065,
            time_to_expiry=time_to_expiry,
            option_type=1 if contract.option_type == OptionType.CALL else -1
        )
        
        # Calculate Greeks
        _, delta, gamma, theta, vega = black_76.calculate_greeks(
            underlying_price=underlying_price,
            strike_price=contract.option_strike,
            interest_rate=0.065,
            time_to_expiry=time_to_expiry,
            volatility=impv,
            option_type=1 if contract.option_type == OptionType.CALL else -1
        )
        
        # Store in custom dict (simplified OptionData)
        option_data = {
            "vt_symbol": contract.vt_symbol,
            "strike": contract.option_strike,
            "expiry": contract.option_expiry,
            "type": contract.option_type,
            "bid": tick.bid_price_1,
            "ask": tick.ask_price_1,
            "mid": mid_price,
            "impv": impv,
            "delta": delta,
            "gamma": gamma,
            "theta": theta,
            "vega": vega,
            "days_to_expiry": days_to_expiry
        }
        
        return option_data
        
    def select_legs(self, expiry: datetime, underlying_price: float):
        """Select legs based on strategy type"""
        
        self.selected_options = {}
        
        if self.strategy_type == "straddle":
            # Find ATM strike
            atm_options = [
                o for o in self.option_chain.values()
                if o["expiry"] == expiry
            ]
            
            if len(atm_options) >= 2:
                # Group by strike
                strike_groups = {}
                for opt in atm_options:
                    if opt["strike"] not in strike_groups:
                        strike_groups[opt["strike"]] = []
                    strike_groups[opt["strike"]].append(opt)
                
                # Find ATM (closest to underlying)
                atm_strike = min(strike_groups.keys(), key=lambda x: abs(x - underlying_price))
                atm_legs = strike_groups[atm_strike]
                
                # Select call and put
                call = next(o for o in atm_legs if o["type"] == OptionType.CALL)
                put = next(o for o in atm_legs if o["type"] == OptionType.PUT)
                
                self.selected_options = {
                    "call": call["vt_symbol"],
                    "put": put["vt_symbol"]
                }
                
        elif self.strategy_type == "strangle":
            # Similar but select OTM strikes
            pass
            
        elif self.strategy_type == "iron_condor":
            # Select 4 legs: OTM put spread + OTM call spread
            pass
            
        self.write_log(f"Selected legs: {list(self.selected_options.keys())}")
        
    def check_entry_signal(self):
        """Check if entry conditions are met"""
        
        # Example: Enter when IV rank is low (for long straddle)
        if not self.am.inited:
            return
            
        # Calculate IV rank (simplified - use historical IV)
        current_iv = self.get_current_iv()
        if not current_iv:
            return
            
        iv_rank = self.calculate_iv_rank(current_iv)
        
        # Entry logic
        if self.strategy_type == "straddle":
            # Long straddle when IV rank is low (expecting expansion)
            if iv_rank < 0.3:  # IV rank below 30%
                self.open_position()
                
        elif self.strategy_type == "strangle":
            # Short strangle when IV rank is high (expecting contraction)
            if iv_rank > 0.7:  # IV rank above 70%
                self.open_position()
                
    def open_position(self):
        """Open option position"""
        
        if not self.selected_options:
            self.write_log("No legs selected")
            return
            
        for leg_name, vt_symbol in self.selected_options.items():
            option = self.option_chain.get(vt_symbol)
            if not option:
                continue
                
            # Get current price
            tick = self.get_tick(vt_symbol)
            if not tick:
                continue
                
            # Determine direction based on strategy and leg type
            if self.strategy_type in ["straddle", "strangle"]:
                # Long strategy: BUY both legs
                direction = Direction.LONG
                volume = self.leg_ratio
            else:
                # Short strategy: SELL both legs
                direction = Direction.SHORT
                volume = self.leg_ratio
            
            # Send order
            vt_orderid = self.send_order(
                vt_symbol=vt_symbol,
                direction=direction,
                offset=Offset.OPEN,
                price=tick.ask_price_1 if direction == Direction.LONG else tick.bid_price_1,
                volume=volume
            )
            
            self.legs_opened.add(leg_name)
            self.entry_premium[vt_symbol] = tick.ask_price_1 if direction == Direction.LONG else tick.bid_price_1
            
            self.write_log(f"Opened {leg_name}: {vt_symbol} {direction.value} {volume} @ {tick.ask_price_1}")
        
        self.position_open = True
        
    def check_exit_signal(self):
        """Check if exit conditions are met"""
        
        # Calculate current PnL
        total_pnl = 0
        for vt_symbol, entry_price in self.entry_premium.items():
            tick = self.get_tick(vt_symbol)
            if not tick:
                continue
                
            current_price = tick.last_price
            pnl_pct = (current_price - entry_price) / entry_price
            total_pnl += pnl_pct
        
        avg_pnl_pct = total_pnl / len(self.entry_premium) if self.entry_premium else 0
        
        # Check stop loss
        if avg_pnl_pct <= -self.stop_loss_pct:
            self.write_log(f"Stop loss triggered: {avg_pnl_pct:.2%}")
            self.close_all_positions()
            return
            
        # Check take profit
        if avg_pnl_pct >= self.take_profit_pct:
            self.write_log(f"Take profit triggered: {avg_pnl_pct:.2%}")
            self.close_all_positions()
            return
            
        # Check delta risk
        self.update_position_greeks()
        if abs(self.position_greeks["delta"]) > self.max_portfolio_delta:
            self.write_log(f"Delta limit breached: {self.position_greeks['delta']}")
            self.adjust_delta()
            
    def update_position_greeks(self):
        """Update portfolio Greeks"""
        
        self.position_greeks = {"delta": 0, "gamma": 0, "theta": 0, "vega": 0}
        
        for vt_symbol in self.selected_options.values():
            option = self.option_chain.get(vt_symbol)
            if not option:
                continue
                
            pos = self.get_pos(vt_symbol)
            if not pos or pos.volume == 0:
                continue
                
            # Add to portfolio Greeks
            self.position_greeks["delta"] += option["delta"] * pos.volume
            self.position_greeks["gamma"] += option["gamma"] * pos.volume
            self.position_greeks["theta"] += option["theta"] * pos.volume
            self.position_greeks["vega"] += option["vega"] * pos.volume
            
    def adjust_delta(self):
        """Delta hedge by adjusting underlying"""
        
        # Calculate hedge quantity
        underlying_tick = self.get_tick(self.underlying_symbol)
        if not underlying_tick:
            return
            
        # Buy/sell underlying to neutralize delta
        hedge_delta = -self.position_greeks["delta"]
        hedge_volume = abs(int(hedge_delta))
        
        if hedge_volume > 0:
            if hedge_delta > 0:
                self.buy(underlying_tick.last_price, hedge_volume, self.underlying_symbol)
            else:
                self.sell(underlying_tick.last_price, hedge_volume, self.underlying_symbol)
                
            self.write_log(f"Delta hedge: {hedge_volume} {self.underlying_symbol}")
            
    def close_all_positions(self):
        """Close all option positions"""
        
        for vt_symbol in list(self.selected_options.values()):
            pos = self.get_pos(vt_symbol)
            if pos and pos.volume > 0:
                if pos.direction == Direction.LONG:
                    self.sell(0, pos.volume, vt_symbol)  # Market order
                else:
                    self.cover(0, pos.volume, vt_symbol)
                    
        self.position_open = False
        self.legs_opened.clear()
        self.entry_premium.clear()
        
    def get_current_iv(self) -> float:
        """Get current implied volatility"""
        # Simplified: average IV of selected options
        if not self.option_chain:
            return None
            
        ivs = [o["impv"] for o in self.option_chain.values() if o.get("impv")]
        return sum(ivs) / len(ivs) if ivs else None
        
    def calculate_iv_rank(self, current_iv: float) -> float:
        """Calculate IV rank"""
        # Simplified: use historical IV percentile
        # In production, use actual IV history from database
        return 0.5  # Placeholder
        
    def on_trade(self, trade):
        self.write_log(f"Trade: {trade.vt_symbol} {trade.direction} {trade.volume} @ {trade.price}")
        self.update_position_greeks()
        self.put_event()
        
    def on_order(self, order):
        self.put_event()
```

---

## Backtesting

```python
# backtest_option_strategy.py
from vnpy_portfoliostrategy import BacktestingEngine
from datetime import datetime
from strategies.dynamic_option_strategy import DynamicOptionStrategy

engine = BacktestingEngine()

engine.set_parameters(
    vt_symbols=[
        "BANKNIFTY.NSE",           # Underlying
        "BANKNIFTY-24DEC-47000-CE.NSE",  # Example options
        "BANKNIFTY-24DEC-47000-PE.NSE",
        # ... more options
    ],
    interval="1m",
    start=datetime(2024, 1, 1),
    end=datetime(2024, 12, 15),
    rate=0.0003,
    slippage=0.5,
    size=15,                      # BANKNIFTY lot size
    pricetick=0.05,
    capital=5_000_000,            # 5 million INR
)

engine.add_strategy(DynamicOptionStrategy, {
    "strategy_type": "straddle",
    "expiry_days_target": 30,
    "strike_distance": "ATM",
    "leg_ratio": 1,
    "underlying_symbol": "BANKNIFTY.NSE",
})

engine.run_backtesting()
df = engine.calculate_result()
engine.calculate_statistics()
engine.show_chart()
```

---

## Data Requirements

| Data | Source | Storage |
|------|--------|---------|
| Underlying (BANKNIFTY) | IB, local provider | Database |
| Option chain (all strikes/expiries) | IB, local provider | Database |
| Historical IV | Calculated or purchased | Database |

**Challenge:** Need complete option chain history for backtesting. Solutions:
1. Record live data with `vnpy_datarecorder`
2. Purchase historical option data
3. Use IB's historical data API (limited)

---

## Summary

| Component | Solution |
|-----------|----------|
| **Base Engine** | `vnpy_portfoliostrategy` |
| **Option Pricing** | `vnpy_optionmaster.pricing` (black_76) |
| **Greeks/IV** | Custom calculation using OptionMaster formulas |
| **Chain Management** | Custom code (select expiry, strikes) |
| **Backtesting** | Portfolio strategy backtester |
| **Live Trading** | Portfolio strategy engine |

**Key Files to Study:**
1. `vnpy_optionmaster/base.py` - OptionData, ChainData classes
2. `vnpy_optionmaster/pricing/black_76.py` - Pricing formulas
3. `vnpy_portfoliostrategy/template.py` - Strategy base
4. `vnpy_portfoliostrategy/backtesting.py` - Backtest engine
