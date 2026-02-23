# Risk Manager Module for VeighNa

<p align="center">
  <img src ="https://vnpy.oss-cn-shanghai.aliyuncs.com/vnpy-logo.png"/>
</p>

<p align="center">
    <img src ="https://img.shields.io/badge/version-2.0.0-blueviolet.svg"/>
    <img src ="https://img.shields.io/badge/platform-windows|linux|macos-yellow.svg"/>
    <img src ="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" />
    <img src ="https://img.shields.io/github/license/vnpy/vnpy.svg?color=orange"/>
</p>

## Description

Pre-trade risk control module for VeighNa framework. Provides a risk rule engine for real-time order validation during trading. All core risk rules are compiled to C extensions using **Cython**, achieving microsecond-level latency for high-frequency trading scenarios.

## Installation

### Environment Requirements

- Python 3.10 or above
- VeighNa 4.0.0 or above
- C++ compiler (for Cython extension compilation)
  - Windows: [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Linux: `sudo apt-get install build-essential`
  - macOS: `xcode-select --install`

### Install via pip

```bash
pip install vnpy_riskmanager
```

### Install from source

```bash
git clone https://github.com/vnpy/vnpy_riskmanager.git
cd vnpy_riskmanager
pip install -e .
```

The `pip install` command will automatically compile the Cython code.

## Features

- **Pre-trade Validation:** Check orders before sending to exchange
- **Rule Engine:** Pluggable risk rule architecture
- **High Performance:** Core rules compiled with Cython (microsecond latency)
- **Real-time Monitoring:** Track risk metrics in real-time
- **Custom Rules:** Create your own risk rules in Python or Cython

## Built-in Risk Rules (5)

| Rule | Description |
|------|-------------|
| `ActiveOrderRule` | Limit on active (working) orders |
| `DailyLimitRule` | Daily order/cancel count limit |
| `DuplicateOrderRule` | Duplicate order detection (same price/size in short time) |
| `OrderSizeRule` | Maximum single order size limit |
| `OrderValidityRule` | Order validity check (price tick, max volume) |

## Usage Example

```python
from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy_ctp import CtpGateway
from vnpy_riskmanager import RiskManagerApp

def main():
    qapp = create_qapp()
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)
    
    main_engine.add_gateway(CtpGateway)
    
    # Add risk manager (auto-starts)
    main_engine.add_app(RiskManagerApp)
    
    main_window = MainWindow(main_engine, event_engine)
    main_window.showMaximized()
    qapp.exec()

if __name__ == "__main__":
    main()
```

## Creating Custom Rules

### Python Rule (Fast Development)

```python
# rules/my_rule.py
from vnpy.trader.object import OrderRequest
from vnpy_riskmanager.template import RuleTemplate

class MyRule(RuleTemplate):
    """My custom rule description"""
    
    name: str = "MyRule"
    
    parameters: dict[str, str] = {
        "max_volume": "Maximum volume per order"
    }
    
    variables: dict[str, str] = {
        "order_count": "Number of orders checked"
    }
    
    def on_init(self) -> None:
        self.max_volume: int = 100
        self.order_count: int = 0
    
    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """
        Core risk logic.
        Return True to allow order, False to reject.
        """
        if req.volume > self.max_volume:
            msg = f"Volume {req.volume} exceeds limit {self.max_volume}"
            self.write_log(msg)
            return False
        
        self.order_count += 1
        self.put_event()  # Update UI
        return True
    
    def on_order(self, order) -> None:
        """Process order feedback"""
        pass
```

### Cython Rule (High Performance)

```cython
# rules/my_rule_cy.pyx
# cython: language_level=3
from vnpy.trader.object cimport OrderRequest
from vnpy_riskmanager.template cimport RuleTemplate

cdef class MyRuleCy(RuleTemplate):
    """Cython rule implementation"""
    cdef public int max_volume
    cdef public int order_count
    
    cpdef void on_init(self):
        self.max_volume = 100
        self.order_count = 0
    
    cpdef bint check_allowed(self, OrderRequest req, str gateway_name):
        if req.volume > self.max_volume:
            self.write_log(f"Volume exceeds limit")
            return False
        self.order_count += 1
        return True

# Python wrapper (required for RiskEngine to discover)
class MyRule(MyRuleCy):
    name: str = "MyRule"
    
    parameters: dict[str, str] = {
        "max_volume": "Maximum volume"
    }
    
    variables: dict[str, str] = {
        "order_count": "Order count"
    }
```

### Compile Cython Rule

```bash
cd rules/
python rule_setup.py build_ext --inplace
```

## Rule Development Files

| File | Purpose |
|------|---------|
| `rules/my_rule.py` | Python rule |
| `rules/my_rule_cy.pyx` | Cython rule |
| `rules/rule_setup.py` | Cython compilation script |

## Performance Comparison

| Rule Type | Latency | Use Case |
|-----------|---------|----------|
| Python | ~10 μs | Low frequency, complex logic |
| Cython | ~0.1 μs | High frequency, simple checks |

## Resources

- **Documentation:** https://www.vnpy.com/docs
- **Forum:** https://www.vnpy.com/forum
- **GitHub:** https://github.com/vnpy/vnpy_riskmanager
