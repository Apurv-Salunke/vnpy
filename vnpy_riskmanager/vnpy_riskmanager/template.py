from typing import TYPE_CHECKING, Any

from vnpy.trader.object import OrderRequest, TickData, OrderData, TradeData, ContractData

if TYPE_CHECKING:
    from .engine import RiskEngine


class RuleTemplate:
    """Risk controlRuletemplate"""

    # Risk controlRuleName
    name: str = ""

    # ParameterfieldandName
    parameters: dict[str, str] = {}

    # VariablefieldandName
    variables: dict[str, str] = {}

    def __init__(self, risk_engine: "RiskEngine", setting: dict) -> None:
        """Constructor"""
        # bindRisk controlEngineObject
        self.risk_engine: RiskEngine = risk_engine

        # AddEnableStatusParameter
        self.active: bool = True

        parameters: dict[str, str] = {
            "active": "EnableRule"
        }
        parameters.update(self.parameters)
        self.parameters = parameters

        # InitializeRule
        self.on_init()

        # UpdateRuleParameter
        self.update_setting(setting)

    def write_log(self, msg: str) -> None:
        """OutputRisk controlLog"""
        self.risk_engine.write_log(msg)

    def update_setting(self, rule_setting: dict) -> None:
        """UpdateRisk controlRuleParameter"""
        for name in self.parameters.keys():
            if name in rule_setting:
                value = rule_setting[name]
                setattr(self, name, value)

    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """CheckwhetherallowOrder"""
        return True

    def on_init(self) -> None:
        """Initialize"""
        pass

    def on_tick(self, tick: TickData) -> None:
        """Market dataPush"""
        pass

    def on_order(self, order: OrderData) -> None:
        """OrderPush"""
        pass

    def on_trade(self, trade: TradeData) -> None:
        """TradePush"""
        pass

    def on_timer(self) -> None:
        """TimerPush（eachsecondstrigger）"""
        pass

    def get_contract(self, vt_symbol: str) -> ContractData | None:
        """QueryContractInfo"""
        return self.risk_engine.get_contract(vt_symbol)

    def put_event(self) -> None:
        """PushDataUpdateEvent"""
        self.risk_engine.put_rule_event(self)

    def get_data(self) -> dict[str, Any]:
        """GetData"""
        parameters: dict[str, Any] = {}
        for name in self.parameters.keys():
            value: Any = getattr(self, name)
            parameters[name] = value

        variables: dict[str, Any] = {}
        for name in self.variables.keys():
            value = getattr(self, name)
            variables[name] = value

        data: dict[str, Any] = {
            "name": self.name,
            "class_name": self.__class__.__name__,
            "parameters": parameters,
            "variables": variables
        }
        return data
