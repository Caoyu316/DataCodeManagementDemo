# Deliberately fragile handover specimen: inspect rather than run.
import csv

with open('/Users/analyst/Desktop/orders.csv') as source:
    amounts = [float(row['amount_chf']) for row in csv.DictReader(source)]
print(sum(amounts))
