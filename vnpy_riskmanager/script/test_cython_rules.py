"""
vnpy_riskmanagermoduleconsistencyTest
"""

import unittest
from typing import Any
from collections import defaultdict

from vnpy.trader.constant import Direction, Offset, OrderType, Status

# ImportPythonRule
from vnpy_riskmanager.rules.active_order_rule import ActiveOrderRule as PyActiveOrderRule
from vnpy_riskmanager.rules.daily_limit_rule import DailyLimitRule as PyDailyLimitRule
from vnpy_riskmanager.rules.duplicate_order_rule import DuplicateOrderRule as PyDuplicateOrderRule
from vnpy_riskmanager.rules.order_size_rule import OrderSizeRule as PyOrderSizeRule
from vnpy_riskmanager.rules.order_validity_rule import OrderValidityRule as PyOrderValidityRule

# ImportCythonRule
try:
    from vnpy_riskmanager.rules.active_order_rule_cy import ActiveOrderRule as CyActiveOrderRule
    from vnpy_riskmanager.rules.daily_limit_rule_cy import DailyLimitRule as CyDailyLimitRule
    from vnpy_riskmanager.rules.duplicate_order_rule_cy import DuplicateOrderRule as CyDuplicateOrderRule
    from vnpy_riskmanager.rules.order_size_rule_cy import OrderSizeRule as CyOrderSizeRule
    from vnpy_riskmanager.rules.order_validity_rule_cy import OrderValidityRule as CyOrderValidityRule
except ImportError:
    print("notFoundCythonRule，pleasefirstcompile")
    exit()


class MockContract:
    """modelsimulateContractData"""

    def __init__(self) -> None:
        self.pricetick: float = 0.1
        self.max_volume: float = 100.0
        self.min_volume: float = 1.0
        self.size: float = 1.0


class MockRiskEngine:
    """modelsimulateRisk controlEngine"""

    def __init__(self) -> None:
        self.contract = MockContract()

    def get_contract(self, vt_symbol: str) -> Any | None:
        if "FAIL" in vt_symbol:
            return None
        return self.contract

    def write_log(self, msg: str) -> None:
        pass

    def put_rule_event(self, rule: Any) -> None:
        pass


class MockOrderRequest:
    """modelsimulateOrderRequest"""

    def __init__(
        self,
        vt_symbol: str,
        volume: float,
        price: float,
        direction: Direction = Direction.LONG,
        offset: Offset = Offset.OPEN,
        type: OrderType = OrderType.LIMIT,
    ):
        self.vt_symbol = vt_symbol
        self.volume = volume
        self.price = price
        self.direction = direction
        self.offset = offset
        self.type = type

    def __str__(self) -> str:
        return f"MockOrderRequest({self.vt_symbol}, {self.volume}@{self.price})"


class MockOrderData:
    """modelsimulateOrderData"""

    def __init__(
        self,
        vt_orderid: str,
        vt_symbol: str,
        status: Status,
    ):
        self.vt_orderid = vt_orderid
        self.vt_symbol = vt_symbol
        self.status = status

    def is_active(self) -> bool:
        return self.status in [Status.SUBMITTING, Status.NOTTRADED, Status.PARTTRADED]


class MockTradeData:
    """modelsimulateTrade data"""

    def __init__(self, vt_tradeid: str, vt_symbol: str):
        self.vt_tradeid = vt_tradeid
        self.vt_symbol = vt_symbol


class BaseRuleConsistencyTest(unittest.TestCase):
    """RuleconsistencyTestbaseClass"""
    py_rule_class: type | None = None
    cy_rule_class: type | None = None

    def setUp(self) -> None:
        """aseachTestsetNewPythonandCythonRuleInstance"""
        if self.py_rule_class is None or self.cy_rule_class is None:
            self.skipTest("RuleconsistencyTestbaseClass")

        self.mock_engine = MockRiskEngine()
        self.py_rule = self.py_rule_class(self.mock_engine, {})
        self.cy_rule = self.cy_rule_class(self.mock_engine, {})

    def assert_state_equal(self, msg: str) -> None:
        """useatcompare twoRuleinsideStatusauxiliaryMethod"""
        py_data = self.py_rule.get_data()
        cy_data = self.cy_rule.get_data()

        # defaultdictunabledirectlycompare
        py_vars = py_data["variables"]
        cy_vars = cy_data["variables"]
        for k, v in py_vars.items():
            if isinstance(v, defaultdict):
                py_vars[k] = dict(v)
        for k, v in cy_vars.items():
            if isinstance(v, defaultdict):
                cy_vars[k] = dict(v)

        self.assertDictEqual(py_data, cy_data, msg)


class TestActiveOrderRuleConsistency(BaseRuleConsistencyTest):
    py_rule_class = PyActiveOrderRule
    cy_rule_class = CyActiveOrderRule

    def test_on_order(self) -> None:
        """Teston_orderconsistency"""
        self.assert_state_equal("initialStatusshouldcomparesame")

        # activeOrder
        order1 = MockOrderData("order1", "IF2401", Status.NOTTRADED)
        self.py_rule.on_order(order1)
        self.cy_rule.on_order(order1)
        self.assert_state_equal("collectToactiveOrderafterStatusshouldcomparesame")

        # inactiveOrder
        order2 = MockOrderData("order1", "IF2401", Status.ALLTRADED)
        self.py_rule.on_order(order2)
        self.cy_rule.on_order(order2)
        self.assert_state_equal("OrderchangeasinactiveafterStatusshouldcomparesame")

    def test_check_allowed(self) -> None:
        """Testcheck_allowedconsistency"""
        req = MockOrderRequest("IF2401", 1, 4000)
        self.assertEqual(
            self.py_rule.check_allowed(req, "CTP"),
            self.cy_rule.check_allowed(req, "CTP")
        )

        self.py_rule.active_order_limit = 0
        self.cy_rule.active_order_limit = 0
        self.assertEqual(
            self.py_rule.check_allowed(req, "CTP"),
            self.cy_rule.check_allowed(req, "CTP")
        )


class TestDailyLimitRuleConsistency(BaseRuleConsistencyTest):
    py_rule_class = PyDailyLimitRule
    cy_rule_class = CyDailyLimitRule

    def test_consistency(self) -> None:
        """Testcompletelifecommandcycleconsistency"""
        self.assert_state_equal("initialStatusshouldcomparesame")

        # NewOrder
        order1 = MockOrderData("order1", "IF2401", Status.NOTTRADED)
        self.py_rule.on_order(order1)
        self.cy_rule.on_order(order1)
        self.assert_state_equal("NewOrderafterStatusshouldcomparesame")

        # CancelOrder
        order2 = MockOrderData("order1", "IF2401", Status.CANCELLED)
        self.py_rule.on_order(order2)
        self.cy_rule.on_order(order2)
        self.assert_state_equal("CancelOrderafterStatusshouldcomparesame")

        # Trade
        trade1 = MockTradeData("trade1", "IF2401")
        self.py_rule.on_trade(trade1)
        self.cy_rule.on_trade(trade1)
        self.assert_state_equal("TradeafterStatusshouldcomparesame")


class TestDuplicateOrderRuleConsistency(BaseRuleConsistencyTest):
    py_rule_class = PyDuplicateOrderRule
    cy_rule_class = CyDuplicateOrderRule

    def test_check_allowed(self) -> None:
        """Testcheck_allowedconsistency"""
        req1 = MockOrderRequest("IF2401", 1, 4000)
        req2 = MockOrderRequest("IF2401", 1, 4000)

        res1_py = self.py_rule.check_allowed(req1, "CTP")
        res1_cy = self.cy_rule.check_allowed(req1, "CTP")
        self.assertEqual(res1_py, res1_cy)
        self.assert_state_equal("FirstRequestafterStatusshouldcomparesame")

        res2_py = self.py_rule.check_allowed(req2, "CTP")
        res2_cy = self.cy_rule.check_allowed(req2, "CTP")
        self.assertEqual(res2_py, res2_cy)
        self.assert_state_equal("firsttwo（Duplicate）RequestafterStatusshouldcomparesame")


class TestOrderSizeRuleConsistency(BaseRuleConsistencyTest):
    py_rule_class = PyOrderSizeRule
    cy_rule_class = CyOrderSizeRule

    def test_check_allowed(self) -> None:
        """Testcheck_allowedconsistency"""
        # legal
        req1 = MockOrderRequest("IF2401", 1, 4000)
        self.assertEqual(
            self.py_rule.check_allowed(req1, "CTP"),
            self.cy_rule.check_allowed(req1, "CTP")
        )

        # VolumeLimit
        req2 = MockOrderRequest("IF2401", 1000, 4000)
        self.assertEqual(
            self.py_rule.check_allowed(req2, "CTP"),
            self.cy_rule.check_allowed(req2, "CTP")
        )

        # pricevalueLimit
        req3 = MockOrderRequest("IF2401", 10, 500000)
        self.assertEqual(
            self.py_rule.check_allowed(req3, "CTP"),
            self.cy_rule.check_allowed(req3, "CTP")
        )


class TestOrderValidityRuleConsistency(BaseRuleConsistencyTest):
    py_rule_class = PyOrderValidityRule
    cy_rule_class = CyOrderValidityRule

    def test_check_allowed(self) -> None:
        """Testcheck_allowedconsistency"""
        # legal
        req1 = MockOrderRequest("IF2401", 10, 4000.1)
        self.assertEqual(
            self.py_rule.check_allowed(req1, "CTP"),
            self.cy_rule.check_allowed(req1, "CTP")
        )

        # illegalContract
        req2 = MockOrderRequest("FAIL2401", 10, 4000.1)
        self.assertEqual(
            self.py_rule.check_allowed(req2, "CTP"),
            self.cy_rule.check_allowed(req2, "CTP")
        )

        # illegalPrice
        req3 = MockOrderRequest("IF2401", 10, 4000.15)
        self.assertEqual(
            self.py_rule.check_allowed(req3, "CTP"),
            self.cy_rule.check_allowed(req3, "CTP")
        )

        # illegalminVolume
        req4 = MockOrderRequest("IF2401", 0.5, 4000.1)
        self.assertEqual(
            self.py_rule.check_allowed(req4, "CTP"),
            self.cy_rule.check_allowed(req4, "CTP")
        )

        # illegalmaxVolume
        req5 = MockOrderRequest("IF2401", 200, 4000.1)
        self.assertEqual(
            self.py_rule.check_allowed(req5, "CTP"),
            self.cy_rule.check_allowed(req5, "CTP")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
