"""Independent extra case. Run: python3 my-check.py repair.py
Before running, predict: a missing baseline stays missing; growth must stop.
Change CODE/YEAR or design another mutation and matching assertions.
"""
import importlib.util
from pathlib import Path
import sys
import pandas as pd
from support import load, compare, check_source

candidate = Path(sys.argv[1] if len(sys.argv)>1 else "repair.py").resolve()
spec = importlib.util.spec_from_file_location("my_candidate", candidate)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
payload = load()
CODE, YEAR = "DEU", "2023"  # Your choice: missing BASELINE, unlike supplied CHE/2024 case.
for record in payload[1]:
    if (record["countryiso3code"], record["date"]) == (CODE, YEAR):
        record["value"] = None  # Local construction; original file stays unchanged.
table = module.extract(payload)
check_source(table, payload)
value = table.loc[(table.country_code==CODE) & (table.year==int(YEAR)), "population"].iloc[0]
assert pd.isna(value), "Missing baseline must not become zero"
try:
    compare(table)
except ValueError as error:
    assert "Missing population" in str(error), "Expected a missingness diagnosis"
else:
    raise AssertionError("Growth with missing baseline must stop")
print("PASS extra case: missing baseline; candidate:", candidate)
