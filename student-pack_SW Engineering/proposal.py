"""CONSTRUCTED teaching proposal; review before accepting. extraction and comparison, with I/O kept in report.py."""
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


def growth_percent(previous, current):
    """Return unrounded percentage change for validated finite numeric scalars.

    Preconditions: previous > 0 and current >= 0. Caller validates these.
    No I/O or mutation. Example: growth_percent(100, 110) returns 10.0.
    """
    return round(100 * (current - previous) / previous, 3)


def compare(table):
    """Return one row per country in code order, with unrounded growth (%).

    Input: six keyed rows from extract; populations in persons. Reject missing
    populations and nonpositive 2023 baselines. Current-year zero is valid.
    Columns: country_code, population_2023, population_2024, increase, growth_pct.
    Preserve input; no file access, printing or network.
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
        rate = growth_percent(previous, current)
        rows.append({"country_code": code, "population_2023": previous,
                     "population_2024": current, "increase": current - previous,
                     "growth_pct": rate})
    return pd.DataFrame(rows)
