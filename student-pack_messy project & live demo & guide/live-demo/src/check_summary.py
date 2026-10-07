"""Independently compare the saved summary with the current input."""
import csv
from decimal import Decimal
from pathlib import Path

project = Path(__file__).resolve().parents[1]

try:
    with (project / "data/raw/orders.csv").open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    # Work in whole cents; do not import the analysis or reuse its result.
    total_cents = 0
    for row in rows:
        cents = Decimal(row["amount_chf"]) * 100
        if not cents.is_finite() or cents != cents.to_integral_value():
            raise ValueError("amounts must contain whole cents")
        total_cents += int(cents)
    if not rows:
        raise ValueError("input contains no orders")
    expected = (
        f"Number of orders: {len(rows)}\n"
        f"Total revenue (CHF): {Decimal(total_cents) / 100:.2f}\n"
        f"Average order value (CHF): {Decimal(total_cents) / 100 / len(rows):.2f}\n"
    )
    actual = (project / "outputs/summary_final.txt").read_text(encoding="utf-8")
    if actual != expected:
        raise ValueError(f"summary differs from the input. Expected:\n{expected}Found:\n{actual}")
except (OSError, ValueError, KeyError, ArithmeticError) as error:
    raise SystemExit(f"FAIL: {error}\nRun python3 src/summarize.py, then check again.")

print("PASS: saved count, revenue and average agree with the input.")
