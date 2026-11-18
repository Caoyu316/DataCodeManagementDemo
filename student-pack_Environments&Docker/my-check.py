"""Independent precision check. Choose a new case BEFORE asking AI.
The seed is constructed, not a World Bank estimate. Modify only these four values.
"""
import math
import sys
from runner import candidate
from validation import load
CODE = "CHE"
PREVIOUS = 300
CURRENT = 400
EXPECTED_PERCENT = 100 / 3  # hand reasoning: increase is one third of baseline
# Alternative: choose DEU, 600 -> 700, expected 100/6. Write your reasoning.

def verify(code):
    table = code.extract(load())
    table.loc[(table.country_code == CODE) & (table.year == 2023), "population"] = PREVIOUS
    table.loc[(table.country_code == CODE) & (table.year == 2024), "population"] = CURRENT
    result = code.compare(table)  # actual selected candidate, including its helper
    actual = result.loc[result.country_code == CODE, "growth_pct"].iloc[0]
    print(f"PRECISION {CODE}: expected {EXPECTED_PERCENT:.12f}; actual {actual:.12f}")
    if not math.isclose(actual, EXPECTED_PERCENT, rel_tol=0, abs_tol=1e-9):
        raise AssertionError("Full-precision contract violated; do not relax the tolerance")
    print("PRECISION PASS (absolute tolerance 1e-9 percentage points)")

if __name__ == "__main__":
    if len(sys.argv)!=2: raise SystemExit("Usage: python3 my-check.py CANDIDATE.py")
    verify(candidate(sys.argv[1]))
