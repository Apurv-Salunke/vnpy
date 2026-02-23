from vnpy.trader.object import OrderRequest, ContractData

from ..template import RuleTemplate


class OrderValidityRule(RuleTemplate):
    """OrderinstructionCheckRisk controlRule"""

    name: str = "OrderinstructionCheck"

    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """CheckwhetherallowOrder"""
        # CheckContractExist
        contract: ContractData | None = self.get_contract(req.vt_symbol)
        if not contract:
            self.write_log(f"ContractCode{req.vt_symbol}notExist：{req}")
            return False

        # CheckminPricechange
        if contract.pricetick > 0:
            pricetick: float = contract.pricetick

            # CalculatePriceAndminchangepricebitsurplusnumber
            remainder: float = req.price % pricetick

            # CheckPriceAndminchangepricebitsurplusnumber，ensurePriceaspricetickIntegertimes（allowtiny error，adaptshouldFloatprecisionproblem）
            if abs(remainder) > 1e-6 and abs(remainder - pricetick) > 1e-6:
                self.write_log(f"Price{req.price}is notContractminchangepricebit{pricetick}Integertimes：{req}")
                return False

        # CheckOrder volumeuplimit
        if contract.max_volume and req.volume > contract.max_volume:
            self.write_log(f"Order volume{req.volume}largeatContractOrder volumeuplimit{contract.max_volume}：{req}")
            return False

        # CheckOrder volumedownlimit
        if req.volume < contract.min_volume:
            self.write_log(f"Order volume{req.volume}smallatContractOrder volumedownlimit{contract.min_volume}：{req}")
            return False

        return True
