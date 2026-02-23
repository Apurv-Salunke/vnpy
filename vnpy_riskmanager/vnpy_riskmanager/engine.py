import importlib
import traceback
from collections.abc import Callable
from typing import Any
from pathlib import Path
from glob import glob
from types import ModuleType

try:
    import winsound
except ImportError:
    winsound = None     # type: ignore

from vnpy.event import Event, EventEngine
from vnpy.trader.event import (
    EVENT_TICK,
    EVENT_ORDER,
    EVENT_TRADE,
    EVENT_TIMER,
    EVENT_LOG
)
from vnpy.trader.object import (
    OrderRequest,
    TickData,
    OrderData,
    TradeData,
    ContractData,
    LogData
)
from vnpy.trader.engine import BaseEngine, MainEngine
from vnpy.trader.utility import load_json, save_json
from vnpy.trader.logger import ERROR

from .template import RuleTemplate
from .base import APP_NAME, EVENT_RISK_RULE, EVENT_RISK_NOTIFY


class RiskEngine(BaseEngine):
    """Risk controlEngine"""

    setting_filename: str = "risk_manager_setting.json"

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        """Constructor"""
        super().__init__(main_engine, event_engine, APP_NAME)

        # RuleClasscollectDict：keyasRuleName，valueas(RuleClass, modulename)
        self.rule_classes: dict[str, tuple[type[RuleTemplate], str]] = {}

        # Risk controlRuleInstance（iterateexecuteCheck）
        self.rules: dict[str, RuleTemplate] = {}

        # Risk controlRuleConfig（FromfileLoad）
        self.setting: dict = load_json(self.setting_filename)

        # Risk controlRulefieldNamemap（useatUIDisplay）
        self.field_name_map: dict = {}

        # cache：logwhichRuleneedneedwhichCallback
        self.tick_rules: list[RuleTemplate] = []
        self.order_rules: list[RuleTemplate] = []
        self.trade_rules: list[RuleTemplate] = []
        self.timer_rules: list[RuleTemplate] = []

        self.load_rules()
        self.register_events()
        self.patch_functions()

    def load_rules(self) -> None:
        """Loadlocaltool"""
        # collectallRuleClass
        path_1: Path = Path(__file__).parent.joinpath("rules")
        self.load_rules_from_folder(path_1, "vnpy_riskmanager.rules")

        path_2: Path = Path.cwd().joinpath("rules")
        self.load_rules_from_folder(path_2, "rules")

        # InstanceizecollectToRuleClass
        for class_name, (rule_class, module_name) in self.rule_classes.items():
            self.add_rule(rule_class)

            self.main_engine.write_log(
                msg=f"Risk controlRule[{class_name}]LoadSuccess，module：{module_name}",
                source="RiskEngine"
            )

    def load_rules_from_folder(self, folder_path: Path, module_name: str) -> None:
        """FromfolderLoadlocaltool"""
        for suffix in ["py", "pyd", "so"]:
            pathname: str = str(folder_path.joinpath(f"*.{suffix}"))

            for filepath in glob(pathname):
                filename: str = Path(filepath).stem

                if suffix in {"pyd", "so"}:
                    filename = filename.split(".")[0]       # todrop specialfixedversionaftersuffix

                name: str = f"{module_name}.{filename}"
                self.load_rules_from_module(name)

    def load_rules_from_module(self, module_name: str) -> None:
        """FrommoduleLoadlocaltool"""
        try:
            module: ModuleType = importlib.import_module(module_name)

            for name in dir(module):
                value: Any = getattr(module, name)
                if (
                    isinstance(value, type)
                    and name.endswith("Rule")
                ):
                    self.rule_classes[name] = (value, module_name)
        except Exception:
            msg: str = f"Risk controlRule[{module_name}]LoadFailed：{traceback.format_exc()}"
            self.main_engine.write_log(msg, level=ERROR, source="RiskEngine")

    def add_rule(self, rule_class: type[RuleTemplate]) -> None:
        """RegisterRule"""
        rule_setting: dict = self.setting.get(rule_class.name, {})
        rule: RuleTemplate = rule_class(self, rule_setting)
        self.rules[rule.name] = rule

        # UpdatefieldNamemap
        self.field_name_map.update(rule.parameters)
        self.field_name_map.update(rule.variables)

    def patch_functions(self) -> None:
        """dynamicreplacemainEngineFunction"""
        self._send_order: Callable[[OrderRequest, str], str] = self.main_engine.send_order
        self.main_engine.send_order = self.send_order

    def register_events(self) -> None:
        """detectRuleneedneedEventClasstypeandRegister"""
        # iterateallRule，detectandcacheneedneedCallbackRule
        for rule in self.rules.values():
            if self.needs_callback(rule, "on_tick"):
                self.tick_rules.append(rule)
            if self.needs_callback(rule, "on_order"):
                self.order_rules.append(rule)
            if self.needs_callback(rule, "on_trade"):
                self.trade_rules.append(rule)
            if self.needs_callback(rule, "on_timer"):
                self.timer_rules.append(rule)

        # pressneedRegister event listener
        if self.tick_rules:
            self.event_engine.register(EVENT_TICK, self.process_tick_event)
        if self.order_rules:
            self.event_engine.register(EVENT_ORDER, self.process_order_event)
        if self.trade_rules:
            self.event_engine.register(EVENT_TRADE, self.process_trade_event)
        if self.timer_rules:
            self.event_engine.register(EVENT_TIMER, self.process_timer_event)

    def needs_callback(self, rule: RuleTemplate, method_name: str) -> bool:
        """detectRulewhetherrewritesomeCallbackMethod"""
        rule_method = getattr(rule, method_name)
        base_method = getattr(RuleTemplate, method_name)
        return rule_method.__func__ is not base_method

    def process_tick_event(self, event: Event) -> None:
        """ProcessMarket dataEvent"""
        tick: TickData = event.data
        for rule in self.tick_rules:
            rule.on_tick(tick)

    def process_order_event(self, event: Event) -> None:
        """ProcessOrderEvent"""
        order: OrderData = event.data
        for rule in self.order_rules:
            rule.on_order(order)

    def process_trade_event(self, event: Event) -> None:
        """ProcessTradeEvent"""
        trade: TradeData = event.data
        for rule in self.trade_rules:
            rule.on_trade(trade)

    def process_timer_event(self, event: Event) -> None:
        """ProcessTimerEvent"""
        for rule in self.timer_rules:
            rule.on_timer()

    def send_order(self, req: OrderRequest, gateway_name: str) -> str:
        """place orderRequestRisk controlCheck"""
        result: bool = self.check_allowed(req, gateway_name)
        if not result:
            return ""

        return self._send_order(req, gateway_name)

    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """Checkwhetherallowplace order"""
        for rule in self.rules.values():
            if (
                rule.active                                         # EnableRule
                and not rule.check_allowed(req, gateway_name)       # CheckRulewhetherallow
            ):
                return False
        return True

    def write_log(self, msg: str) -> None:
        """OutputRisk controlLog"""
        log: LogData = LogData(
            msg="Orderbyintercept，" + msg,
            level=ERROR,
            gateway_name=APP_NAME,
        )
        self.event_engine.put(Event(EVENT_LOG, log))

        # PushRisknotificationEvent
        self.event_engine.put(Event(EVENT_RISK_NOTIFY, msg))

        # OutputinterceptLogafterplay sound
        if winsound:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)

    def get_contract(self, vt_symbol: str) -> ContractData | None:
        """QueryContractInfo（provideRulecall）"""
        return self.main_engine.get_contract(vt_symbol)

    def put_rule_event(self, rule: RuleTemplate) -> None:
        """PushRuleEvent"""
        data: dict[str, Any] = rule.get_data()
        event: Event = Event(EVENT_RISK_RULE, data)
        self.event_engine.put(event)

    def update_rule_setting(self, rule_name: str, rule_setting: dict) -> None:
        """UpdatespecifiedRuleParameter"""
        self.setting[rule_name] = rule_setting

        # UpdateToRuleObject
        rule: RuleTemplate = self.rules[rule_name]
        rule.update_setting(rule_setting)
        rule.put_event()

        # Save ConfigTofile
        save_json(self.setting_filename, self.setting)

    def get_all_rule_names(self) -> list[str]:
        """GetallRuleClassname"""
        return list(self.rules.keys())

    def get_rule_data(self, rule_name: str) -> dict[str, Any]:
        """GetspecifiedRuleData"""
        rule: RuleTemplate = self.rules[rule_name]
        return rule.get_data()

    def get_field_name(self, field: str) -> str:
        """GetfieldName"""
        name: str = self.field_name_map.get(field, field)
        return name
