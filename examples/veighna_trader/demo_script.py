from time import sleep

from vnpy_scripttrader import ScriptEngine


def run(engine: ScriptEngine):
    """
    Main function description for script strategy:
    1. The only parameter is the ScriptEngineScriptEngineobject，used to complete query and request operations
    2. This function runs in a separate thread, different from event-driven strategy modules
    3. whileloop maintenance，useengine.strategy_activestatus to determine，controlled exit

    Examples of script strategy applications:
    1. Custom basket order execution algorithm
    2. Hedging strategy between stock index futures and a basket of stocks
    3. Cross-exchange arbitrage for domestic and international commodities
    4. Custom portfolio index market monitoring and notification
    5. Stock market scanning and stock selection trading strategies (top picks)
    6. And more~~~
    """
    vt_symbols = ["IF2506.CFFEX", "rb2510.SHFE"]

    # Subscribe to market data
    engine.subscribe(vt_symbols)

    # Get contract info
    for vt_symbol in vt_symbols:
        contract = engine.get_contract(vt_symbol)
        msg = f"Contract info，{contract}"
        engine.write_log(msg)

    # Keep running，usestrategy_activeto determine whether to exit
    while engine.strategy_active:
        # Poll for market data
        for vt_symbol in vt_symbols:
            tick = engine.get_tick(vt_symbol)
            msg = f"Latest market data, {tick}"
            engine.write_log(msg)

        # Wait3secondsbefore next iteration
        sleep(3)
