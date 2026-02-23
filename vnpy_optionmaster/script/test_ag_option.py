"""Implied volatilityCalculateTestscript"""
import sys
import io
from collections.abc import Callable

from vnpy_optionmaster.pricing import (
    binomial_tree, black_76, black_scholes,
    binomial_tree_cython,
    black_76_cython,
    black_scholes_cython
)


# TestData
TEST_DATA: list[dict] = [
    # deep OTMOption
    {"symbol": "ag2601P14700", "price": 22.0, "underlying": 16143.0, "strike": 14700, "r": 0.02, "t": 0.0167, "cp": -1, "category": "deep OTM"},
    {"symbol": "ag2601P14800", "price": 27.0, "underlying": 16143.0, "strike": 14800, "r": 0.02, "t": 0.0167, "cp": -1, "category": "deep OTM"},
    {"symbol": "ag2601P14900", "price": 32.5, "underlying": 16143.0, "strike": 14900, "r": 0.02, "t": 0.0167, "cp": -1, "category": "deep OTM"},
    {"symbol": "ag2601P15000", "price": 41.0, "underlying": 16143.0, "strike": 15000, "r": 0.02, "t": 0.0167, "cp": -1, "category": "deep OTM"},
    # at-the-moneyOption
    {"symbol": "ag2601P16100", "price": 350.0, "underlying": 16143.0, "strike": 16100, "r": 0.02, "t": 0.0167, "cp": -1, "category": "at-the-money"},
    {"symbol": "ag2601C16100", "price": 340.0, "underlying": 16143.0, "strike": 16100, "r": 0.02, "t": 0.0167, "cp": 1, "category": "at-the-money"},
    # deep ITMOption
    {"symbol": "ag2601C14000", "price": 2200.0, "underlying": 16143.0, "strike": 14000, "r": 0.02, "t": 0.0167, "cp": 1, "category": "deep ITM"},
    {"symbol": "ag2601C13000", "price": 3200.0, "underlying": 16143.0, "strike": 13000, "r": 0.02, "t": 0.0167, "cp": 1, "category": "deep ITM"},
    {"symbol": "ag2601P19000", "price": 2920.0, "underlying": 16143.0, "strike": 19000, "r": 0.02, "t": 0.0167, "cp": -1, "category": "deep ITM"},
]


def verify_impv(model_name: str, calc_price_func: Callable, calc_impv_func: Callable, use_n: bool = False) -> dict:
    """VerifyImplied volatilityCalculateresult"""
    results = {"success": 0, "total": len(TEST_DATA), "details": []}

    for data in TEST_DATA:
        # CalculateImplied volatility
        if use_n:
            impv = calc_impv_func(
                price=data["price"],
                f=data["underlying"],
                k=data["strike"],
                r=data["r"],
                t=data["t"],
                cp=data["cp"]
            )
        else:
            impv = calc_impv_func(
                price=data["price"],
                s=data["underlying"],
                k=data["strike"],
                r=data["r"],
                t=data["t"],
                cp=data["cp"]
            )

        # reversetoVerify
        if impv > 0:
            if use_n:
                calc_price = calc_price_func(
                    f=data["underlying"],
                    k=data["strike"],
                    r=data["r"],
                    t=data["t"],
                    v=impv,
                    cp=data["cp"]
                )
            else:
                calc_price = calc_price_func(
                    s=data["underlying"],
                    k=data["strike"],
                    r=data["r"],
                    t=data["t"],
                    v=impv,
                    cp=data["cp"]
                )
            error = abs(calc_price - data["price"])
            success = error < 2.0
        else:
            error = data["price"]
            success = False

        if success:
            results["success"] += 1 # type: ignore

        results["details"].append({ # type: ignore
            "symbol": data["symbol"],
            "category": data["category"],
            "impv": impv,
            "error": error,
            "success": success
        })

    return results


def print_results(model_name: str, results: dict) -> None:
    """printTestresult"""
    print(f"\n{'='*70}")
    print(f"{model_name} Testresult")
    print(f"{'='*70}")
    print(f"{'Contract':15s} {'Classtype':8s} {'Implied volatility':>12s} {'error':>10s} {'Status':>6s}")
    print("-" * 70)

    for d in results["details"]:
        status = "✓" if d["success"] else "✗"
        print(f"{d['symbol']:15s} {d['category']:8s} {d['impv']:12.4f} {d['error']:10.2f} {status:>6s}")

    rate = results["success"] / results["total"] * 100
    print("-" * 70)
    print(f"Successrate: {results['success']}/{results['total']} ({rate:.1f}%)")


def main() -> None:
    """mainFunction"""
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 70)
    print("OptionPricing ModelImplied volatilityCalculateTest")
    print("=" * 70)

    # Testbinomialtreemodel
    bt_results = verify_impv(
        "Binomial Tree",
        binomial_tree.calculate_price,
        binomial_tree.calculate_impv,
        use_n=True
    )
    print_results("Binomial Tree (binomialtree)", bt_results)

    # Test Black-76 model
    b76_results = verify_impv(
        "Black-76",
        black_76.calculate_price,
        black_76.calculate_impv,
        use_n=False
    )
    print_results("Black-76", b76_results)

    # Test Black-Scholes model
    bs_results = verify_impv(
        "Black-Scholes",
        black_scholes.calculate_price,
        black_scholes.calculate_impv,
        use_n=False
    )
    print_results("Black-Scholes", bs_results)

    # Test Cython version
    print(f"\n{'='*70}")
    print("Cython versionTest")
    print(f"{'='*70}")

    # Testbinomialtreemodel (Cython)
    bt_cython_results = verify_impv(
        "Binomial Tree Cython",
        binomial_tree_cython.calculate_price,
        binomial_tree_cython.calculate_impv,
        use_n=True
    )
    print_results("Binomial Tree Cython (binomialtree)", bt_cython_results)

    # Test Black-76 model (Cython)
    b76_cython_results = verify_impv(
        "Black-76 Cython",
        black_76_cython.calculate_price,
        black_76_cython.calculate_impv,
        use_n=False
    )
    print_results("Black-76 Cython", b76_cython_results)

    # Test Black-Scholes model (Cython)
    bs_cython_results = verify_impv(
        "Black-Scholes Cython",
        black_scholes_cython.calculate_price,
        black_scholes_cython.calculate_impv,
        use_n=False
    )
    print_results("Black-Scholes Cython", bs_cython_results)

    # summaryTotal
    print(f"\n{'='*70}")
    print("summaryTotalstatistics")
    print(f"{'='*70}")
    print(f"{'model':25s} {'Successrate':>15s}")
    print("-" * 45)
    for name, results in [
        ("Binomial Tree", bt_results),
        ("Black-76", b76_results),
        ("Black-Scholes", bs_results),
        ("Binomial Tree Cython", bt_cython_results),
        ("Black-76 Cython", b76_cython_results),
        ("Black-Scholes Cython", bs_cython_results),
    ]:
        rate = results["success"] / results["total"] * 100
        print(f"{name:25s} {results['success']}/{results['total']} ({rate:5.1f}%)")


if __name__ == "__main__":
    main()
