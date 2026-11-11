"""Manual starter: move compare's display into the caller (two TODOs)."""
import pandas as pd
from validation import validate_envelope, check_table


def extract(payload):
    """Return six sorted country-year rows from the bounded Week 8 response.

    Keep source code/name/value associations and null as missing. Reject invalid
    envelopes and duplicate/missing keys. Do not mutate payload; no I/O.
    """
    rows = []
    for record in validate_envelope(payload):
        rows.append({"country_code": record["countryiso3code"],
                     "country_name": record["country"]["value"],
                     "year": int(record["date"]),
                     "population": record["value"]})
    return check_table(pd.DataFrame(rows))


def compare(table):
    """Initial behavior: print the formatted comparison and return None.

    Target after TODOs: return one row per country in code order, with
    unrounded numeric growth (%); let the caller format and print.

    Input: six keyed rows from extract; populations in persons. Reject missing
    populations and nonpositive 2023 baselines. Current-year zero is valid.
    Columns: country_code, population_2023, population_2024, increase, growth_pct.
    Both versions preserve input and use no file access or network.
    Only the target version does no printing.
    """
    table = check_table(table)
    if table.population.isna().any():
        raise ValueError("Missing population: cannot compute complete growth comparison")
    rows = []
    for code in sorted(table.country_code.unique()):
        country = table[table.country_code == code]
        previous = country.loc[country.year == 2023, "population"].iloc[0]
        current = country.loc[country.year == 2024, "population"].iloc[0]
        if previous <= 0:
            raise ValueError("Baseline must be positive for percentage growth")
        rate = 100 * (current - previous) / previous
        rows.append({"country_code": code, "population_2023": previous,
                     "population_2024": current, "increase": current - previous,
                     "growth_pct": rate})
    result = pd.DataFrame(rows)
    # TODO A: replace this print with return result.
    print(result.to_string(index=False, float_format=lambda value: f"{value:.3f}"))

if __name__ == "__main__":
    from validation import load
    # TODO B: assign the returned table, then print it here with the same format.
    compare(extract(load()))
