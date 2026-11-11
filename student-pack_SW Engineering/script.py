"""Teaching adaptation of Week 8; correct report, tangled responsibilities."""
import pandas as pd
from validation import load, validate_envelope, check_table
payload = load()
rows = []
for record in validate_envelope(payload):
    rows.append({"country_code": record["countryiso3code"],
                 "country_name": record["country"]["value"],
                 "year": int(record["date"]), "population": record["value"]})
table = check_table(pd.DataFrame(rows))
if table.population.isna().any():
    raise ValueError("Missing population: cannot compute complete growth comparison")
rows = []
for code in sorted(table.country_code.unique()):
    country = table[table.country_code == code]
    previous = country.loc[country.year == 2023, "population"].iloc[0]
    current = country.loc[country.year == 2024, "population"].iloc[0]
    if previous <= 0:
        raise ValueError("Baseline must be positive for percentage growth")
    rows.append({"country_code": code, "population_2023": previous,
                 "population_2024": current, "increase": current - previous,
                 "growth_pct": 100 * (current - previous) / previous})
result = pd.DataFrame(rows)
print(result.to_string(index=False, float_format=lambda value: f"{value:.3f}"))
