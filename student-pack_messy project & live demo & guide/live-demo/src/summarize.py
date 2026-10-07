"""Summarize all orders; recreate the output from the preserved input."""
import csv
from decimal import Decimal
from pathlib import Path

project = Path(__file__).resolve().parents[1]
with (project / "data/raw/orders.csv").open(newline="", encoding="utf-8") as source:
    amounts = [Decimal(row["amount_chf"]) for row in csv.DictReader(source)]

number_of_orders = len(amounts)
revenue = sum(amounts)
average_order_value = revenue / number_of_orders

summary = (
    f"Number of orders: {number_of_orders}\n"
    f"Total revenue (CHF): {revenue:.2f}\n"
    f"Average order value (CHF): {average_order_value:.2f}\n"
)
(project / "outputs").mkdir(exist_ok=True)
(project / "outputs/summary_final.txt").write_text(summary, encoding="utf-8")
print(summary, end="")
