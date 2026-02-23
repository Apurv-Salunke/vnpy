# Persistence and Recovery in VeighNa

Analysis of process exit/restart capabilities and how to add resume functionality.

---

## Current State: Limited Persistence

### What IS Persisted

| Component | Persisted | Location | Mechanism |
|-----------|-----------|----------|-----------|
| **CTA Strategy Parameters** | ✅ Yes | `cta_strategy_setting.json` | Auto-save on add/update |
| **CTA Strategy Variables** | ✅ Yes | `cta_strategy_data.json` | Sync on trade |
| **OptionMaster Settings** | ✅ Yes | `option_master_setting.json` | Auto-save |
| **Algo Parameters** | ❌ No | - | Not implemented |
| **Algo State** | ❌ No | - | Not implemented |
| **Active Orders** | ❌ No | - | Lost on restart |
| **Active Algorithms** | ❌ No | - | Lost on restart |

---

## CTA Strategy Persistence (Works)

### Setting Persistence

**File:** `.vntrader/cta_strategy_setting.json`

```json
{
  "DualMa_Rb2401": {
    "class_name": "DualMaStrategy",
    "vt_symbol": "RB2401.SHFE",
    "setting": {
      "fast_window": 10,
      "slow_window": 30
    }
  }
}
```

**Load on Startup:**
```python
# vnpy_ctastrategy/engine.py
def load_strategy_setting(self) -> None:
    """Load setting file"""
    self.strategy_setting = load_json(self.setting_filename)
    
    for strategy_name, strategy_config in self.strategy_setting.items():
        self.add_strategy(
            strategy_config["class_name"],
            strategy_name,
            strategy_config["vt_symbol"],
            strategy_config["setting"]
        )
```

### Variable Persistence

**File:** `.vntrader/cta_strategy_data.json`

```json
{
  "DualMa_Rb2401": {
    "pos": 10,
    "fast_ma0": 3850.5,
    "slow_ma0": 3820.2,
    "fast_ma1": 3845.0,
    "slow_ma1": 3815.5
  }
}
```

**Sync on Trade:**
```python
def process_trade_event(self, event: Event) -> None:
    trade: TradeData = event.data
    strategy = self.orderid_strategy_map.get(trade.vt_orderid)
    
    if strategy:
        # Update position
        if trade.direction == Direction.LONG:
            strategy.pos += trade.volume
        else:
            strategy.pos -= trade.volume
        
        # Sync to file
        self.sync_strategy_data(strategy)

def sync_strategy_data(self, strategy: CtaTemplate) -> None:
    """Sync strategy data into json file"""
    data = strategy.get_variables()
    data.pop("inited")   # Don't save status
    data.pop("trading")
    
    self.strategy_data[strategy.strategy_name] = data
    save_json(self.data_filename, self.strategy_data)
```

### Recovery Flow (CTA)

```
Process Restart
    ↓
CtaEngine.__init__()
    ↓
load_strategy_setting()  ← Load config from JSON
    ↓
add_strategy()           ← Recreate strategy instances
    ↓
load_strategy_data()     ← Load variables from JSON
    ↓
Strategy variables restored (pos, ma values, etc.)
    ↓
BUT: No order history, no active orders
```

**Limitations:**
- ✅ Strategy parameters restored
- ✅ Strategy variables restored (pos, indicators)
- ❌ Order history lost
- ❌ Trade history lost (but can query from database)
- ❌ Active stop orders lost

---

## Algo Trading Persistence (NOT Implemented)

### Current State

```python
# vnpy_algotrading/engine.py
class AlgoEngine(BaseEngine):
    def __init__(self, ...):
        self.algo_templates: dict[str, type] = {}
        self.algos: dict[str, AlgoTemplate] = {}  # In-memory only
        self.symbol_algo_map: dict[str, set] = {}
        self.orderid_algo_map: dict[str, AlgoTemplate] = {}
        
        # NO load/save methods!
```

**What happens on restart:**

```
Process Running
    ↓
Algo Running: TWAP buying 10,000 shares
    - traded = 3,500
    - traded_price = 2449.50
    - active_orders = {...}
    ↓
⚡ Process Exit (crash/restart)
    ↓
Process Restart
    ↓
AlgoEngine.__init__()
    ↓
❌ No algo instances restored
❌ No state recovered
❌ Child orders still active at exchange (orphaned!)
```

### Problems

1. **Algo state lost:** `traded`, `traded_price`, `timer_count` all reset
2. **Child orders orphaned:** Orders sent to exchange still active but algo gone
3. **No tracking:** Can't resume because no record of what was being done
4. **Double execution risk:** If you restart same algo, might execute again

---

## Adding Persistence to AlgoEngine

### Solution Architecture

```python
# Enhanced AlgoEngine with persistence

class AlgoEngine(BaseEngine):
    def __init__(self, ...):
        super().__init__(...)
        
        # Existing
        self.algos: dict[str, AlgoTemplate] = {}
        
        # NEW: Persistence
        self.algo_settings: dict = {}  # Persisted config
        self.algo_states: dict = {}    # Persisted state
    
    def init_engine(self) -> None:
        """Initialize on startup"""
        self.load_algo_settings()   # ← NEW: Load config
        self.load_algo_states()     # ← NEW: Load state
    
    def close(self) -> None:
        """Save before exit"""
        self.save_algo_settings()   # ← NEW
        self.save_algo_states()     # ← NEW
        self.cancel_all()           # ← Important: Clean up orders
```

### Algo State to Persist

```python
class AlgoTemplate:
    # ... existing fields ...
    
    def get_state(self) -> dict:
        """Get algorithm state for persistence"""
        return {
            "algo_name": self.algo_name,
            "template_name": self.__class__.__name__,
            "vt_symbol": self.vt_symbol,
            "direction": self.direction.value,
            "offset": self.offset.value,
            "price": self.price,
            "volume": self.volume,
            "status": self.status.value,
            "traded": self.traded,
            "traded_price": self.traded_price,
            "active_orderids": list(self.active_orders.keys()),
            # Algo-specific variables
            **self.get_variables()
        }
    
    def restore_state(self, state: dict) -> None:
        """Restore algorithm state from persistence"""
        # Basic fields already set in __init__
        self.status = AlgoStatus(state["status"])
        self.traded = state["traded"]
        self.traded_price = state["traded_price"]
        
        # Note: Can't restore active_orders (already sent to exchange)
        # Need special handling
```

### Implementation

```python
# algo_engine.py
import json
from pathlib import Path
from vnpy.trader.utility import load_json, save_json

class AlgoEngine(BaseEngine):
    setting_filename = "algo_trading_setting.json"
    state_filename = "algo_trading_state.json"
    
    def load_algo_settings(self) -> None:
        """Load algo config from file"""
        self.algo_settings = load_json(self.setting_filename)
        
        # Recreate algo instances
        for algo_name, config in self.algo_settings.items():
            self._create_algo_from_config(config, is_restart=True)
    
    def save_algo_settings(self) -> None:
        """Save algo config to file"""
        save_json(self.setting_filename, self.algo_settings)
    
    def load_algo_states(self) -> None:
        """Load algo state from file"""
        self.algo_states = load_json(self.state_filename)
        
        # Restore state to each algo
        for algo_name, state in self.algo_states.items():
            algo = self.algos.get(algo_name)
            if algo:
                algo.restore_state(state)
    
    def save_algo_states(self) -> None:
        """Save algo state to file"""
        for algo_name, algo in self.algos.items():
            if algo.status in {AlgoStatus.RUNNING, AlgoStatus.PAUSED}:
                self.algo_states[algo_name] = algo.get_state()
        
        save_json(self.state_filename, self.algo_states)
    
    def start_algo(self, template_name, vt_symbol, direction, offset, price, volume, setting) -> str:
        """Start algorithm"""
        # Create algo instance
        algo = self._create_algo(...)
        
        # Save config
        self.algo_settings[algo.algo_name] = {
            "template_name": template_name,
            "vt_symbol": vt_symbol,
            "direction": direction.value,
            "offset": offset.value,
            "price": price,
            "volume": volume,
            "setting": setting
        }
        self.save_algo_settings()
        
        return algo.algo_name
    
    def _create_algo_from_config(self, config: dict, is_restart: bool = False) -> AlgoTemplate:
        """Create algo from saved config"""
        template_class = self.algo_templates[config["template_name"]]
        
        # Parse direction/offset from string
        direction = Direction(config["direction"])
        offset = Offset(config["offset"])
        
        algo = template_class(
            self,
            config["algo_name"],
            config["vt_symbol"],
            direction,
            offset,
            config["price"],
            config["volume"],
            config["setting"]
        )
        
        self.algos[algo.algo_name] = algo
        self.symbol_algo_map[vt_symbol].add(algo)
        
        return algo
    
    def cancel_all(self) -> None:
        """Cancel all active orders before shutdown"""
        for algo in list(self.algos.values()):
            if algo.status in {AlgoStatus.RUNNING, AlgoStatus.PAUSED}:
                algo.cancel_all()
                algo.stop()
```

---

## Recovery Strategies

### Option 1: Full Auto-Restore

```python
# On restart, automatically resume all algos

def load_algo_settings(self) -> None:
    self.algo_settings = load_json(self.setting_filename)
    
    for algo_name, config in self.algo_settings.items():
        algo = self._create_algo_from_config(config)
        
        # Auto-resume if was running
        if config.get("was_running", False):
            algo.resume()  # Continue execution
```

**Pros:**
- Seamless recovery
- No manual intervention

**Cons:**
- Risk of double-execution if not careful
- Market conditions may have changed

### Option 2: Manual Review & Resume

```python
# On restart, show paused algos for review

def load_algo_settings(self) -> None:
    self.algo_settings = load_json(self.setting_filename)
    
    for algo_name, config in self.algo_settings.items():
        algo = self._create_algo_from_config(config)
        
        # Start in PAUSED state for review
        algo.status = AlgoStatus.PAUSED
        self.write_log(f"算法 {algo_name} 已恢复，请检查后手动继续")
```

**Pros:**
- User can verify market conditions
- Safer

**Cons:**
- Requires manual intervention

### Option 3: Hybrid (Recommended)

```python
def load_algo_settings(self) -> None:
    self.algo_settings = load_json(self.setting_filename)
    
    for algo_name, config in self.algo_settings.items():
        algo = self._create_algo_from_config(config)
        
        # Check if algo finished naturally
        if config.get("status") == "FINISHED":
            self.write_log(f"算法 {algo_name} 已完成，不恢复")
            continue
        
        # Check elapsed time
        last_update = config.get("last_update")
        if last_update:
            elapsed = datetime.now() - last_update
            if elapsed > timedelta(hours=1):  # Stale
                self.write_log(f"算法 {algo_name} 已过期，不恢复")
                continue
        
        # Restore state
        state = self.algo_states.get(algo_name, {})
        algo.restore_state(state)
        
        # Pause for review
        algo.status = AlgoStatus.PAUSED
        self.write_log(f"算法 {algo_name} 已恢复，状态：{algo.traded}/{algo.volume}")
```

---

## Handling Orphaned Orders

**Problem:** Orders sent by algo still active at exchange after crash.

### Solution 1: Cancel All on Startup

```python
def init_engine(self) -> None:
    """Initialize engine"""
    # Cancel all active orders from previous session
    all_orders = self.main_engine.get_all_active_orders()
    
    for order in all_orders:
        self.main_engine.cancel_order(order.create_cancel_request(), order.gateway_name)
        self.write_log(f"撤销遗留订单：{order.vt_orderid}")
```

**Pros:** Clean slate
**Cons:** Might cancel unrelated orders

### Solution 2: Track and Cancel Algo Orders

```python
def load_algo_states(self) -> None:
    self.algo_states = load_json(self.state_filename)
    
    # Collect all orphaned order IDs
    orphaned_orderids = set()
    for state in self.algo_states.values():
        orphaned_orderids.update(state.get("active_orderids", []))
    
    # Cancel them
    for vt_orderid in orphaned_orderids:
        order = self.main_engine.get_order(vt_orderid)
        if order and order.is_active():
            self.main_engine.cancel_order(order.create_cancel_request(), order.gateway_name)
```

### Solution 3: Gateway-Level Cleanup

```python
# In each gateway
class BaseGateway:
    def connect(self, setting: dict) -> None:
        """On connect, query and cancel orphaned orders"""
        # Query open orders
        open_orders = self.query_open_orders()
        
        # Cancel orders from vnpy (tagged with reference)
        for order in open_orders:
            if order.reference.startswith("Algo_"):
                self.cancel_order(order.create_cancel_request())
```

---

## Complete Implementation Example

### Enhanced AlgoTemplate

```python
# template.py
class AlgoTemplate:
    def __init__(self, ...):
        # ... existing init ...
        self.created_at = datetime.now()
        self.last_update = datetime.now()
    
    def get_state(self) -> dict:
        """Get state for persistence"""
        return {
            "algo_name": self.algo_name,
            "template_name": self.__class__.__name__,
            "vt_symbol": self.vt_symbol,
            "direction": self.direction.value,
            "offset": self.offset.value,
            "price": self.price,
            "volume": self.volume,
            "status": self.status.value,
            "traded": self.traded,
            "traded_price": self.traded_price,
            "active_orderids": list(self.active_orders.keys()),
            "created_at": self.created_at.isoformat(),
            "last_update": self.last_update.isoformat(),
            **self.get_variables()
        }
    
    def restore_state(self, state: dict) -> None:
        """Restore state"""
        self.status = AlgoStatus(state["status"])
        self.traded = state["traded"]
        self.traded_price = state["traded_price"]
        self.created_at = datetime.fromisoformat(state["created_at"])
        self.last_update = datetime.fromisoformat(state["last_update"])
        
        # Note: active_orderids are NOT restored (orders already at exchange)
```

### Enhanced AlgoEngine

```python
# engine.py
class AlgoEngine(BaseEngine):
    setting_filename = "algo_trading_setting.json"
    state_filename = "algo_trading_state.json"
    
    def init_engine(self) -> None:
        """Initialize on startup"""
        self.load_algo_templates()
        self.register_event()
        
        # NEW: Load persisted algos
        self.load_algo_settings()
        self.load_algo_states()
        
        # NEW: Cancel orphaned orders
        self.cancel_orphaned_orders()
        
        self.write_log("算法引擎初始化完成")
    
    def close(self) -> None:
        """Save and cleanup on shutdown"""
        self.stop_all()
        self.save_algo_settings()
        self.save_algo_states()
    
    def start_algo(self, template_name, vt_symbol, direction, offset, price, volume, setting) -> str:
        """Start algorithm with persistence"""
        algo = self._create_algo(template_name, vt_symbol, direction, offset, price, volume, setting)
        
        # Save config
        self.algo_settings[algo.algo_name] = {
            "template_name": template_name,
            "vt_symbol": vt_symbol,
            "direction": direction.value,
            "offset": offset.value,
            "price": price,
            "volume": volume,
            "setting": setting,
            "created_at": algo.created_at.isoformat()
        }
        save_json(self.setting_filename, self.algo_settings)
        
        algo.start()
        return algo.algo_name
    
    def stop_algo(self, algo_name: str) -> None:
        """Stop algorithm"""
        algo = self.algos.get(algo_name)
        if algo:
            algo.stop()
            
            # Update status in config
            if algo_name in self.algo_settings:
                self.algo_settings[algo_name]["status"] = "STOPPED"
                save_json(self.setting_filename, self.algo_settings)
    
    def cancel_orphaned_orders(self) -> None:
        """Cancel orders from previous session"""
        all_orders = self.main_engine.get_all_active_orders()
        
        for order in all_orders:
            # Cancel orders with algo reference
            if order.reference.startswith("Algo_"):
                self.main_engine.cancel_order(order.create_cancel_request(), order.gateway_name)
                self.write_log(f"撤销遗留算法订单：{order.vt_orderid}")
```

---

## Summary

| Feature | CTA Strategy | Algo Trading |
|---------|--------------|--------------|
| **Parameter persistence** | ✅ Yes | ❌ No (can add) |
| **Variable persistence** | ✅ Yes | ❌ No (can add) |
| **Auto-restore on restart** | ✅ Yes | ❌ No (can add) |
| **Order cleanup** | ⚠️ Manual | ❌ No (can add) |

**To add resume capability to AlgoEngine:**

1. Add `save_algo_settings()` / `load_algo_settings()`
2. Add `save_algo_states()` / `load_algo_states()`
3. Implement `AlgoTemplate.get_state()` / `restore_state()`
4. Add orphaned order cleanup on startup
5. Decide recovery strategy (auto/manual/hybrid)

**Estimated effort:** ~200-300 lines of code

**Files to modify:**
- `vnpy_algotrading/engine.py`
- `vnpy_algotrading/template.py`
- Create: `algo_trading_setting.json`, `algo_trading_state.json`
