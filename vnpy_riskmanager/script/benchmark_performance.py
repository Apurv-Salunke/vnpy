"""
performanceTest：Pythonversion vs Cythonversion
forratioallRisk controlRule check_allowed Functionperformancedifference
"""
import time
import sys
from typing import Any


class MockContract:
    """modelsimulateContractObject"""

    def __init__(self) -> None:
        self.pricetick: float = 0.1
        self.max_volume: float = 100.0
        self.min_volume: float = 1.0
        self.size: float = 1.0


class MockRiskEngine:
    """modelsimulateRisk controlEngine"""

    def __init__(self) -> None:
        self.logs: list[str] = []
        self.events: list[Any] = []
        self.contract = MockContract()

    def write_log(self, msg: str) -> None:
        """logLog"""
        self.logs.append(msg)

    def put_rule_event(self, rule: Any) -> None:
        """PushRuleEvent"""
        pass

    def get_contract(self, vt_symbol: str) -> Any | None:
        """QueryContract"""
        if "FAIL" in vt_symbol:
            return None
        return self.contract


class MockOrderRequest:
    """modelsimulateOrderRequest"""

    def __init__(
        self,
        symbol: str = "IF2401",
        volume: float = 1.0,
        price: float = 4000.0,
        reference: str = ""
    ):
        self.vt_symbol: str = symbol
        self.volume: float = volume
        self.price: float = price
        self.reference: str = reference or f"{symbol}_{volume}@{price}"

        # modelsimulate enumClasstype
        class Type:
            value = "LIMIT"
        class Direction:
            value = "LONG"
        class Offset:
            value = "OPEN"

        self.type = Type()
        self.direction = Direction()
        self.offset = Offset()

    def __str__(self) -> str:
        return self.reference


def benchmark_rule(
    rule_class: type,
    rule_name: str,
    iterations: int,
    config: dict[str, Any]
) -> dict:
    """performanceTestFunction"""
    print(f"\n{'='*60}")
    print(f"Test {rule_name} - {config['name']}")
    print(f"{'='*60}")

    # CreateRuleInstance
    mock_engine = MockRiskEngine()
    setting = {"active": True, **config["settings"]}
    rule = rule_class(mock_engine, setting)

    # warmup
    warmup_req = config["requests_pass"][0]
    for _ in range(1000):
        rule.check_allowed(warmup_req, "CTP")

    print(f"Iterationcount: {iterations:,}")

    # --- scenario1: Checkthroughpast ---
    print("\nscenario1: Checkthroughpast (fast path)")
    config["setup_pass"](rule)
    requests_pass = config["requests_pass"]

    start_time = time.perf_counter()
    for i in range(iterations):
        rule.check_allowed(requests_pass[i % len(requests_pass)], "CTP")
    elapsed_time = time.perf_counter() - start_time

    ops_per_sec = iterations / elapsed_time
    time_per_call_ns = (elapsed_time / iterations) * 1_000_000_000

    print(f"  Totalconsumetime: {elapsed_time:.4f} seconds")
    print(f"  eachtimescall: {time_per_call_ns:.2f} acceptseconds")
    print(f"  throughputvolume: {ops_per_sec:,.0f} times/seconds")

    result_1 = {
        "elapsed_time": elapsed_time,
        "ops_per_sec": ops_per_sec,
        "time_per_call_ns": time_per_call_ns
    }

    # --- scenario2: CheckFailed ---
    print("\nscenario2: CheckFailed (triggerLog)")
    config["setup_fail"](rule)
    requests_fail = config["requests_fail"]
    mock_engine.logs.clear()

    fail_iterations = iterations // 10
    start_time = time.perf_counter()
    for i in range(fail_iterations):
        rule.check_allowed(requests_fail[i % len(requests_fail)], "CTP")
    elapsed_time = time.perf_counter() - start_time

    ops_per_sec = fail_iterations / elapsed_time
    time_per_call_ns = (elapsed_time / fail_iterations) * 1_000_000_000

    print(f"  Totalconsumetime: {elapsed_time:.4f} seconds")
    print(f"  eachtimescall: {time_per_call_ns:.2f} acceptseconds")
    print(f"  throughputvolume: {ops_per_sec:,.0f} times/seconds")
    print(f"  LogVolume: {len(mock_engine.logs):,}")

    result_2 = {
        "elapsed_time": elapsed_time,
        "ops_per_sec": ops_per_sec,
        "time_per_call_ns": time_per_call_ns
    }

    return {"scenario_1": result_1, "scenario_2": result_2}


def compare_results(py_results: dict, cy_results: dict, rule_name: str) -> None:
    """forratioandOutputresult"""
    print("\n" + "="*60)
    print(f"performanceforcompareTotal - {rule_name}")
    print("="*60)

    py_time_1 = py_results["scenario_1"]["time_per_call_ns"]
    cy_time_1 = cy_results["scenario_1"]["time_per_call_ns"]
    speedup_1 = py_time_1 / cy_time_1 if cy_time_1 else float('inf')

    print("\nscenario1: Checkthroughpast (fast path)")
    print("-" * 60)
    print(f"Pythonversion:  {py_time_1:>8.2f} acceptseconds/times  "
          f"{py_results['scenario_1']['ops_per_sec']:>12,.0f} times/seconds")
    print(f"Cythonversion:  {cy_time_1:>8.2f} acceptseconds/times  "
          f"{cy_results['scenario_1']['ops_per_sec']:>12,.0f} times/seconds")
    print(f"Performance improvement:    {speedup_1:.2f}x")

    py_time_2 = py_results["scenario_2"]["time_per_call_ns"]
    cy_time_2 = cy_results["scenario_2"]["time_per_call_ns"]
    speedup_2 = py_time_2 / cy_time_2 if cy_time_2 else float('inf')

    print("\nscenario2: CheckFailed (triggerLog)")
    print("-" * 60)
    print(f"Pythonversion:  {py_time_2:>8.2f} acceptseconds/times  "
          f"{py_results['scenario_2']['ops_per_sec']:>12,.0f} times/seconds")
    print(f"Cythonversion:  {cy_time_2:>8.2f} acceptseconds/times  "
          f"{cy_results['scenario_2']['ops_per_sec']:>12,.0f} times/seconds")
    print(f"Performance improvement:    {speedup_2:.2f}x")

    print("\n" + "="*60)
    avg_speedup = (speedup_1 + speedup_2) / 2
    print(f"averagePerformance improvement: {avg_speedup:.2f}x")

    if avg_speedup >= 3.0:
        rating = "[+++] excellent"
    elif avg_speedup >= 2.0:
        rating = "[++] goodgood"
    elif avg_speedup >= 1.5:
        rating = "[+] noterror"
    else:
        rating = "[=] adaptin"
    print(f"performancerating: {rating}")


def main() -> bool:
    """mainTestworkflow"""
    print("="*60)
    print("vnpy_riskmanager performancebenchmarkTest")
    print("Pythonversion vs Cythonversion")
    print("="*60)

    # --- ImportallRule ---
    try:
        from vnpy_riskmanager.rules.active_order_rule import ActiveOrderRule as PyActiveOrderRule
        from vnpy_riskmanager.rules.active_order_rule_cy import ActiveOrderRule as CyActiveOrderRule
        from vnpy_riskmanager.rules.daily_limit_rule import DailyLimitRule as PyDailyLimitRule
        from vnpy_riskmanager.rules.daily_limit_rule_cy import DailyLimitRule as CyDailyLimitRule
        from vnpy_riskmanager.rules.duplicate_order_rule import DuplicateOrderRule as PyDuplicateOrderRule
        from vnpy_riskmanager.rules.duplicate_order_rule_cy import DuplicateOrderRule as CyDuplicateOrderRule
        from vnpy_riskmanager.rules.order_size_rule import OrderSizeRule as PyOrderSizeRule
        from vnpy_riskmanager.rules.order_size_rule_cy import OrderSizeRule as CyOrderSizeRule
        from vnpy_riskmanager.rules.order_validity_rule import OrderValidityRule as PyOrderValidityRule
        from vnpy_riskmanager.rules.order_validity_rule_cy import OrderValidityRule as CyOrderValidityRule
        print("\n[OK] SuccessImportallRulemodule (Python and Cython)")
    except ImportError as e:
        print(f"\n[FAIL] unableImportRulemodule: {e}")
        print("\npleasefirstcompile Cython module:")
        print("  python setup.py build_ext --inplace")
        return False

    # --- TestConfig ---
    iterations = 100000

    rules_to_test = [
        {
            "name": "activeOrderCheck",
            "py_class": PyActiveOrderRule,
            "cy_class": CyActiveOrderRule,
            "settings": {"active_order_limit": 50},
            "setup_pass": lambda rule: setattr(rule, 'active_order_count', 0),
            "requests_pass": [MockOrderRequest(f"IF{i}") for i in range(100)],
            "setup_fail": lambda rule: setattr(rule, 'active_order_count', rule.active_order_limit),
            "requests_fail": [MockOrderRequest(f"IF{i}") for i in range(100)],
        },
        {
            "name": "eachdaysuplimitCheck",
            "py_class": PyDailyLimitRule,
            "cy_class": CyDailyLimitRule,
            "settings": {"total_order_limit": 200},
            "setup_pass": lambda rule: setattr(rule, 'total_order_count', 0),
            "requests_pass": [MockOrderRequest(f"RB{i}") for i in range(100)],
            "setup_fail": lambda rule: setattr(rule, 'total_order_count', rule.total_order_limit),
            "requests_fail": [MockOrderRequest(f"RB{i}") for i in range(100)],
        },
        {
            "name": "DuplicateorderCheck",
            "py_class": PyDuplicateOrderRule,
            "cy_class": CyDuplicateOrderRule,
            "settings": {"duplicate_order_limit": 10},
            "setup_pass": lambda rule: rule.on_init(),
            "requests_pass": [MockOrderRequest(reference=f"req_{i}") for i in range(100)],
            "setup_fail": lambda rule: rule.on_init(),
            "requests_fail": [MockOrderRequest(reference="DUPLICATE_REQ")] * 20,
        },
        {
            "name": "OrderscaleCheck",
            "py_class": PyOrderSizeRule,
            "cy_class": CyOrderSizeRule,
            "settings": {"order_volume_limit": 50, "order_value_limit": 2_000_000},
            "setup_pass": lambda rule: None,
            "requests_pass": [MockOrderRequest(volume=10, price=4000)],
            "setup_fail": lambda rule: None,
            "requests_fail": [MockOrderRequest(volume=60, price=4000)], # Exceeds volume
        },
        {
            "name": "OrderinstructionCheck",
            "py_class": PyOrderValidityRule,
            "cy_class": CyOrderValidityRule,
            "settings": {},
            "setup_pass": lambda rule: None,
            "requests_pass": [MockOrderRequest(price=4000.1)],  # Valid pricetick
            "setup_fail": lambda rule: None,
            "requests_fail": [MockOrderRequest(price=4000.15)], # Invalid pricetick
        },
    ]

    print(f"\nTestConfig: {iterations:,} timesIteration/scenario")

    # --- RunningallTest ---
    for config in rules_to_test:
        py_results = benchmark_rule(config["py_class"], "Python version", iterations, config)
        cy_results = benchmark_rule(config["cy_class"], "Cython version", iterations, config)
        compare_results(py_results, cy_results, config["name"])

    return True


if __name__ == "__main__":
    success = main()

    if success:
        print("\n" + "="*60)
        print("allTestCompleted！")
        print("="*60)
        sys.exit(0)
    else:
        sys.exit(1)
